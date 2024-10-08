"""Raytracing DAG for incident irradiance."""
from pollination_dsl.dag import Inputs, DAG, task
from dataclasses import dataclass

from pollination.honeybee_radiance.coefficient import DaylightCoefficientNoSkyMatrix


@dataclass
class IncidentIrradianceRayTracing(DAG):

    # inputs
    radiance_parameters = Inputs.str(
        description='The radiance parameters for ray tracing',
        default='-ab 1'
    )

    octree_file = Inputs.file(
        description='A Radiance octree file.',
        extensions=['oct']
    )

    model_name = Inputs.str(
        description='Model file name. This is useful for naming the final results.'
    )

    grid_name = Inputs.str(
        description='Sensor grid file name. This is useful to rename the final result '
        'file to {grid_name}.res'
    )

    sensor_count = Inputs.int(
        description='The maximum number of grid points.',
        spec={'type': 'integer', 'minimum': 1}
    )

    sensor_grid = Inputs.file(
        description='Sensor grid file.',
        extensions=['pts']
    )

    sky_dome = Inputs.file(
        description='Path to sky dome file.'
    )

    @task(template=DaylightCoefficientNoSkyMatrix)
    def total_sky(
        self,
        radiance_parameters=radiance_parameters,
        fixed_radiance_parameters='-aa 0.0 -I -c 1',
        sensor_count=sensor_count,
        sky_dome=sky_dome,
        sensor_grid=sensor_grid,
        conversion='0.265 0.670 0.065',  # divide by 179,
        output_format='f',
        scene_file=octree_file,
        model_name=model_name,
        name=grid_name
    ):
        return [
            {
                'from': DaylightCoefficientNoSkyMatrix()._outputs.result_file,
                'to': '../../../../results/states/{{self.model_name}}/{{self.name}}.dc'
            }
        ]
