
from pathlib import Path

from json_schema_for_humans.generate import generate_from_filename
from json_schema_for_humans.generation_configuration import GenerationConfiguration

if __name__ == "__main__":

    # Configure the docs
    config = GenerationConfiguration(
        minify=False,
        copy_css=True,
        expand_buttons=True,
        show_breadcrumbs=False,
        show_toc=True,
        collapse_long_descriptions=False,
        collapse_long_examples=False,
        description_is_markdown=True,
        examples_as_yaml=True,
        # template_md_options={
        #     "badge_as_image": True,
        #     "show_heading_numbers": False
        # },
        # template_name="md_nested"
    )

    # Using the json file and config from above, create the docs web page
    base_path = Path(__file__).parent.parent
    generate_from_filename(
        base_path / "windIO" / "plant" / "wind_energy_system.yaml",
        "source/plant_schema_doc.html",
        config=config
    )
    generate_from_filename(
        base_path / "windIO" / "turbine" / "IEAontology_schema.yaml",
        "source/turbine_schema_doc.html",
        config=config
    )
