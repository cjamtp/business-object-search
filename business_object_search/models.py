"""Data models for Business Rules and related entities."""

from datetime import date
from typing import List, Dict, Any, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field, validator

import config


class RuleCategory(str, Enum):
    """Categories of business rules."""
    
    DATA = "data"
    VALIDATION = "validation"
    CALCULATION = "calculation"
    PROCESS = "process"
    REPORTING = "reporting"
    COMPLIANCE = "compliance"


class ObligationLevel(str, Enum):
    """Level of obligation for a rule."""
    
    MANDATORY = "mandatory"
    CONDITIONAL = "conditional"
    OPTIONAL = "optional"


class DataElement(BaseModel):
    """Model representing a data element that rules can apply to."""
    
    element_id: str = Field(..., description="Unique identifier for the data element")
    name: str = Field(..., description="Name of the data element")
    description: Optional[str] = Field(None, description="Description of the data element")
    data_type: Optional[str] = Field(None, description="Data type of the element")
    domain: Optional[str] = Field(None, description="Business domain of the element")
    
    class Config:
        """Pydantic model configuration."""
        
        schema_extra = {
            "example": {
                "element_id": "DE001",
                "name": "customer_income",
                "description": "Annual customer income",
                "data_type": "decimal",
                "domain": "customer"
            }
        }


class RuleBase(BaseModel):
    """Base model for a business rule with common fields."""
    
    name: str = Field(..., description="Concise descriptive name")
    description: str = Field(..., description="Complete rule statement")
    category: RuleCategory = Field(..., description="Rule category")
    obligation_level: ObligationLevel = Field(..., description="Level of obligation")
    data_elements: List[str] = Field(default_factory=list, description="List of data fields this rule applies to")
    conditions: List[str] = Field(default_factory=list, description="Array of conditions when this rule applies")
    actions: List[str] = Field(default_factory=list, description="Array of required actions")
    exceptions: List[str] = Field(default_factory=list, description="Array of exceptions")
    thresholds: List[str] = Field(default_factory=list, description="Any numerical limits or thresholds")
    validation_logic: Optional[str] = Field(None, description="Formal expression of validation where applicable")
    source_reference: Optional[str] = Field(None, description="Exact article/paragraph numbers")
    effective_date: Optional[date] = Field(None, description="When rule takes effect, if specified")
    related_rules: List[str] = Field(default_factory=list, description="IDs of related or dependent rules")
    
    @validator('category', pre=True)
    def validate_category(cls, v):
        """Validate rule category."""
        if isinstance(v, str):
            if v.lower() not in [cat.lower() for cat in config.RULE_CATEGORIES]:
                raise ValueError(f"Invalid category: {v}. Must be one of {config.RULE_CATEGORIES}")
            # Return standardized case
            for cat in config.RULE_CATEGORIES:
                if v.lower() == cat.lower():
                    return cat
        return v
    
    @validator('obligation_level', pre=True)
    def validate_obligation_level(cls, v):
        """Validate obligation level."""
        if isinstance(v, str):
            if v.lower() not in [level.lower() for level in config.OBLIGATION_LEVELS]:
                raise ValueError(f"Invalid obligation level: {v}. Must be one of {config.OBLIGATION_LEVELS}")
            # Return standardized case
            for level in config.OBLIGATION_LEVELS:
                if v.lower() == level.lower():
                    return level
        return v


class RuleCreate(RuleBase):
    """Model for creating a new rule."""
    
    pass


class Rule(RuleBase):
    """Model representing a complete business rule."""
    
    rule_id: str = Field(..., description="Unique identifier")
    created_at: Optional[date] = Field(None, description="When the rule was created")
    updated_at: Optional[date] = Field(None, description="When the rule was last updated")
    
    class Config:
        """Pydantic model configuration."""
        
        schema_extra = {
            "example": {
                "rule_id": "R001",
                "name": "Income Validation",
                "description": "Customer income must be greater than zero and verified with supporting documentation",
                "category": "validation",
                "obligation_level": "mandatory",
                "data_elements": ["customer_income"],
                "conditions": ["customer_application_submitted = true"],
                "actions": ["validate_income_documentation", "flag_if_income_zero_or_negative"],
                "exceptions": ["customer_type = 'student_loan'"],
                "thresholds": [],
                "validation_logic": "customer_income > 0",
                "source_reference": "Lending Policy v2.1, Section 3.4.2",
                "effective_date": "2025-01-01",
                "related_rules": [],
                "created_at": "2025-03-23",
                "updated_at": "2025-03-23"
            }
        }


class RuleUpdate(BaseModel):
    """Model for updating an existing rule (all fields optional)."""
    
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[RuleCategory] = None
    obligation_level: Optional[ObligationLevel] = None
    data_elements: Optional[List[str]] = None
    conditions: Optional[List[str]] = None
    actions: Optional[List[str]] = None
    exceptions: Optional[List[str]] = None
    thresholds: Optional[List[str]] = None
    validation_logic: Optional[str] = None
    source_reference: Optional[str] = None
    effective_date: Optional[date] = None
    related_rules: Optional[List[str]] = None
    
    @validator('category', pre=True)
    def validate_category(cls, v):
        """Validate rule category."""
        if v is None:
            return v
        if isinstance(v, str):
            if v.lower() not in [cat.lower() for cat in config.RULE_CATEGORIES]:
                raise ValueError(f"Invalid category: {v}. Must be one of {config.RULE_CATEGORIES}")
            # Return standardized case
            for cat in config.RULE_CATEGORIES:
                if v.lower() == cat.lower():
                    return cat
        return v
    
    @validator('obligation_level', pre=True)
    def validate_obligation_level(cls, v):
        """Validate obligation level."""
        if v is None:
            return v
        if isinstance(v, str):
            if v.lower() not in [level.lower() for level in config.OBLIGATION_LEVELS]:
                raise ValueError(f"Invalid obligation level: {v}. Must be one of {config.OBLIGATION_LEVELS}")
            # Return standardized case
            for level in config.OBLIGATION_LEVELS:
                if v.lower() == level.lower():
                    return level
        return v


class RuleFilter(BaseModel):
    """Model for filtering rules in search queries."""
    
    rule_id: Optional[str] = None
    name: Optional[str] = None
    category: Optional[RuleCategory] = None
    obligation_level: Optional[ObligationLevel] = None
    data_element: Optional[str] = None
    effective_date_from: Optional[date] = None
    effective_date_to: Optional[date] = None
    search_text: Optional[str] = None
    related_to_rule_id: Optional[str] = None


class RuleValidationResult(BaseModel):
    """Model representing the result of rule validation."""
    
    rule_id: str
    name: str
    passed: bool
    message: Optional[str] = None
    required_actions: List[str] = Field(default_factory=list)


class EvaluationContext(BaseModel):
    """Context data for rule evaluation."""
    
    data: Dict[str, Any] = Field(default_factory=dict)
    applied_rules: List[str] = Field(default_factory=list)
    validation_results: List[RuleValidationResult] = Field(default_factory=list)
