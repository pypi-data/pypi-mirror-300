from pydantic import BaseModel, Field
from typing_extensions import Literal, Optional

from Schemas_ses.Schemas_ses.enumeration.enums import StudiesLevel, LocalType
from Schemas_ses.Schemas_ses.models.model import AnnexeModel
from Schemas_ses.Schemas_ses.type.types import Year


class TeacherFurniture(BaseModel):
    teacher_desk_with_chair: int = Field(..., description="Number of teacher's desks with chairs")
    cupboard_or_closet: int = Field(..., description="Number of cupboards or closets")


Good_or_bad = Literal['Bon / Acceptable', 'Mauvais']


class Office(AnnexeModel):
    name: str
    study_years: StudiesLevel
    local_type: LocalType
    year_of_commissioning: Year
    is_unused: bool
    wall_material: Literal["En dur", "Semi-dur / banco", "Autre: Planche / bambou", "Sans mur"]
    wall_condition: Good_or_bad
    roof_material: Literal["Tôles", "Tuiles / Fibro ciment / Dalles", "Banco", "Paille", "Sans toit"]
    roof_condition: Good_or_bad
    door_material: Literal["Métallique", "Tôle / Bois", "Non installées"]
    wall_nature: Literal["Persiennes", "Volets", "Claustras", "Non installées"]
    funding: Literal["Collectivités locales", "APE", "Aide extérieure", "Autres / Non déterminé"]
    teacher_furniture: TeacherFurniture
    # add student_furniture
    surface_area: float = Field(..., description="Surface area of the office (in m²)")
    blackboard: int = Field(..., description="Number of blackboards")


class OfficeAndFurniture(AnnexeModel):
    """Se réfère à la section Locaux Et Mobiliers"""
    offices: Optional[list[Office]]

