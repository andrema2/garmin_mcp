"""
Data management functions for Garmin Connect MCP Server
"""
import logging
from typing import Optional

from garmin_mcp.utils.decorators import handle_garmin_errors
from garmin_mcp.utils.serialization import serialize_response
from garmin_mcp.utils.garmin_async import call_garmin
from garmin_mcp.utils.validation import (
    validate_date,
    validate_positive_number,
    sanitize_string,
)

logger = logging.getLogger(__name__)


def register_tools(app):
    """Register all data management tools with the MCP server app"""
    
    @app.tool()
    @handle_garmin_errors
    async def add_body_composition(
        date: str,
        weight: float,
        percent_fat: Optional[float] = None,
        percent_hydration: Optional[float] = None,
        visceral_fat_mass: Optional[float] = None,
        bone_mass: Optional[float] = None,
        muscle_mass: Optional[float] = None,
        basal_met: Optional[float] = None,
        active_met: Optional[float] = None,
        physique_rating: Optional[int] = None,
        metabolic_age: Optional[float] = None,
        visceral_fat_rating: Optional[int] = None,
        bmi: Optional[float] = None
    ) -> str:
        """Add body composition data
        
        Args:
            date: Date in YYYY-MM-DD format
            weight: Weight in kg (must be positive)
            percent_fat: Body fat percentage (optional)
            percent_hydration: Hydration percentage (optional)
            visceral_fat_mass: Visceral fat mass (optional)
            bone_mass: Bone mass (optional)
            muscle_mass: Muscle mass (optional)
            basal_met: Basal metabolic rate (optional)
            active_met: Active metabolic rate (optional)
            physique_rating: Physique rating (optional)
            metabolic_age: Metabolic age (optional)
            visceral_fat_rating: Visceral fat rating (optional)
            bmi: Body Mass Index (optional)
            
        Returns:
            Addition result or error message
        """
        date = validate_date(date, "date")
        weight = validate_positive_number(weight, "weight", allow_zero=False)
        
        # Validate optional numeric parameters if provided
        if percent_fat is not None:
            validate_positive_number(percent_fat, "percent_fat", allow_zero=True)
        if percent_hydration is not None:
            validate_positive_number(percent_hydration, "percent_hydration", allow_zero=True)
        if visceral_fat_mass is not None:
            validate_positive_number(visceral_fat_mass, "visceral_fat_mass", allow_zero=True)
        if bone_mass is not None:
            validate_positive_number(bone_mass, "bone_mass", allow_zero=True)
        if muscle_mass is not None:
            validate_positive_number(muscle_mass, "muscle_mass", allow_zero=True)
        if basal_met is not None:
            validate_positive_number(basal_met, "basal_met", allow_zero=True)
        if active_met is not None:
            validate_positive_number(active_met, "active_met", allow_zero=True)
        if metabolic_age is not None:
            validate_positive_number(metabolic_age, "metabolic_age", allow_zero=True)
        if bmi is not None:
            validate_positive_number(bmi, "bmi", allow_zero=True)
        
        result = await call_garmin(
            "add_body_composition",
            date,
            weight=weight,
            percent_fat=percent_fat,
            percent_hydration=percent_hydration,
            visceral_fat_mass=visceral_fat_mass,
            bone_mass=bone_mass,
            muscle_mass=muscle_mass,
            basal_met=basal_met,
            active_met=active_met,
            physique_rating=physique_rating,
            metabolic_age=metabolic_age,
            visceral_fat_rating=visceral_fat_rating,
            bmi=bmi
        )
        return serialize_response(result) if not isinstance(result, str) else result
    
    @app.tool()
    @handle_garmin_errors
    async def set_blood_pressure(
        systolic: int,
        diastolic: int,
        pulse: int,
        notes: Optional[str] = None
    ) -> str:
        """Set blood pressure values
        
        Args:
            systolic: Systolic pressure (top number, must be positive)
            diastolic: Diastolic pressure (bottom number, must be positive)
            pulse: Pulse rate (must be positive)
            notes: Optional notes (will be sanitized)
            
        Returns:
            Result or error message
        """
        systolic = int(validate_positive_number(systolic, "systolic", allow_zero=False))
        diastolic = int(validate_positive_number(diastolic, "diastolic", allow_zero=False))
        pulse = int(validate_positive_number(pulse, "pulse", allow_zero=False))
        
        if notes:
            notes = sanitize_string(notes, "notes")

        result = await call_garmin("set_blood_pressure", systolic, diastolic, pulse, notes=notes)
        return serialize_response(result) if not isinstance(result, str) else result
    
    @app.tool()
    @handle_garmin_errors
    async def add_hydration_data(
        value_in_ml: int,
        cdate: str,
        timestamp: str
    ) -> str:
        """Add hydration data
        
        Args:
            value_in_ml: Amount of liquid in milliliters (must be positive)
            cdate: Date in YYYY-MM-DD format
            timestamp: Timestamp in YYYY-MM-DDThh:mm:ss.sss format
            
        Returns:
            Addition result or error message
        """
        value_in_ml = int(validate_positive_number(value_in_ml, "value_in_ml", allow_zero=True))
        cdate = validate_date(cdate, "cdate")
        timestamp = sanitize_string(timestamp, "timestamp")

        result = await call_garmin("add_hydration_data", value_in_ml=value_in_ml, cdate=cdate, timestamp=timestamp)
        return serialize_response(result) if not isinstance(result, str) else result

    return app
