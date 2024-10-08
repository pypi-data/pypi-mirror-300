from pollination_dsl.dag import Inputs, DAG, task, Outputs
from dataclasses import dataclass
from pollination.honeybee_radiance.sky import CreateSkyDome

from pollination.path.read import ReadJSONList

# input/output alias
from pollination.alias.inputs.radiancepar import rad_par_annual_input

from ._irradiance_calc import IncidentIrradianceEntryPoint


@dataclass
class SandboxSolarIrradianceEntryPoint(DAG):
    """Sandbox Solar irradiance entry point."""

    # inputs
    radiance_parameters = Inputs.str(
        description='Radiance parameters for ray tracing.',
        default='-ad 5000 -lw 2e-05',
        alias=rad_par_annual_input
    )

    models = Inputs.file(
        description='A JSON array of the names for the HBJSON models to be simulated.'
    )

    model_folder = Inputs.folder(
        description='A folder containing the HBJSON models to be simulated.'
    )

    @task(template=CreateSkyDome)
    def create_sky_dome(self):
        """Create sky dome for daylight coefficient studies."""
        return [
            {'from': CreateSkyDome()._outputs.sky_dome, 'to': 'resources/sky.dome'}
        ]

    @task(template=ReadJSONList)
    def read_model_list(self, src=models):
        return [
            {
                'from': ReadJSONList()._outputs.data,
                'description': 'List of model information.'
            }
        ]

    @task(
        template=IncidentIrradianceEntryPoint,
        needs=[
            create_sky_dome, read_model_list
        ],
        loop=read_model_list._outputs.data,
        sub_folder='initial_results/{{item.name}}',  # create a subfolder for each grid
        sub_paths={'model': '{{item.name}}.hbjson'}  # sub_path for sensor_grid arg
    )
    def incident_irradiance_calc(
        self,
        model=model_folder,
        radiance_parameters=radiance_parameters,
        sky_dome=create_sky_dome._outputs.sky_dome,
        model_name='{{item.name}}'
    ):
        pass

    results = Outputs.folder(
        source='results', description='Folder with raw result files (.ill) that '
        'contain matrices of total irradiance.'
    )
