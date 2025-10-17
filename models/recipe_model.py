from pydantic import BaseModel, Field
from typing import List, Optional


class Ingredient(BaseModel):
    name: str = Field(..., description="Nom de l'ingrédient")
    quantity: float = Field(..., description="Quantité nécessaire")
    unit: str = Field(..., description="Unité de mesure (g, ml, pièce, cuillère, etc.)")


class Recipe(BaseModel):
    name: str = Field(..., description="Nom du plat")
    description: Optional[str] = Field(None, description="Description courte du plat")
    servings: int = Field(default=4, description="Nombre de portions")
    prep_time_minutes: Optional[int] = Field(None, description="Temps de préparation en minutes")
    cook_time_minutes: Optional[int] = Field(None, description="Temps de cuisson en minutes")
    ingredients: List[Ingredient] = Field(..., description="Liste des ingrédients avec quantités")
    steps: List[str] = Field(..., description="Étapes de préparation numérotées")


class RecipeRequest(BaseModel):
    ingredients: List[str] = Field(..., description="Liste des ingrédients disponibles", min_length=1)
    number_of_recipes: int = Field(default=1, description="Nombre de recettes à générer", ge=1, le=5)
    dietary_restrictions: Optional[List[str]] = Field(None, description="Restrictions alimentaires (végétarien, sans gluten, etc.)")


class RecipeResponse(BaseModel):
    recipes: List[Recipe] = Field(..., description="Liste des recettes générées")
    energy_usage: float = Field(..., description="Consommation énergétique en Wh")
    metrics: Optional[dict] = None
