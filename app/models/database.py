# from sqlalchemy import Column, Integer, String, DateTime, Text
# from sqlalchemy.ext.declarative import declarative_base
# from datetime import datetime

# Base = declarative_base()

# class FallComplianceEvent(Base):
#     """Simple model for fall compliance events"""
#     __tablename__ = 'fall_compliance_events'
    
#     id = Column(Integer, primary_key=True)
#     event_date = Column(DateTime)
#     patient_id = Column(String(255))
#     event_type = Column(String(255))
#     compliance_status = Column(String(255))
#     notes = Column(Text)
#     created_at = Column(DateTime, default=datetime.utcnow)

# class FallIncidentPrimary(Base):
#     """Simple model for fall incidents"""
#     __tablename__ = 'fall_incidents_primary'
    
#     id = Column(Integer, primary_key=True)
#     incident_date = Column(DateTime)
#     patient_id = Column(String(255))
#     incident_type = Column(String(255))
#     severity = Column(String(255))
#     location = Column(String(255))
#     description = Column(Text)
#     outcome = Column(String(255))
#     created_at = Column(DateTime, default=datetime.utcnow)


from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class FallIncidentPrimary(Base):
    """Model representing primary fall incident records"""
    __tablename__ = 'fall_incidents_primary'

    ID = Column(Integer, primary_key=True)
    DATE = Column(DateTime)
    NAME = Column(String)
    ROOM = Column(String)
    DAY_OF_THE_WEEK = Column(String)
    TIME = Column(String)
    INCIDENT_LOCATION = Column(String)
    INJURIES = Column(String)
    CAUSE = Column(String)
    INTERVENTIONS = Column(Text)
    RNAO_ASSESSMENT = Column(Text)
    INCIDENTREPORT = Column(Text)
    HIR = Column(Text)
    PHYSICIANREF = Column(Text)
    POACONTACTED = Column(Text)
    PTREF = Column(Text)
    TRANSFER_TO_HOSPITAL = Column(String)
    POSTFALLNOTES = Column(Text)
    POSTFALLNOTESCOLOR = Column(String)
    SIGNIFICANT_INJURY_FLAG = Column(Boolean)
    NON_COMPLIANCE_FLAG = Column(Boolean)
    ISCAUSEUPDATED = Column(Boolean)
    ISHIRUPDATED = Column(Boolean)
    ISHOSPITALUPDATED = Column(Boolean)
    ISINCIDENTREPORTUPDATED = Column(Boolean)
    ISINTERVENTIONSUPDATED = Column(Boolean)
    ISPHYSCIANREFUPDATED = Column(Boolean)
    ISPHYSICIANREFUPDATED = Column(Boolean)
    ISPOACONTACTEDUPDATED = Column(Boolean)
    ISPOSTFALLNOTESUPDATED = Column(Boolean)
    ISPTREFUPDATED = Column(Boolean)
    NURSENAME = Column(String)
    HIR_INITIAL = Column(Text)
    HIR_FOLLOWUPS = Column(Text)
    POACONTACTEDDETAILS = Column(Text)
    PHYSICIANREFDETAILS = Column(Text)
    HOSPITALNAME = Column(String)
    DIETICIANREF = Column(Text)
    POSTFALLHUDDLECOMPLETED = Column(Boolean)
    FLOOR = Column(String)
    TIMEOFDAY = Column(String)
    CREATED_AT = Column(DateTime, default=datetime.utcnow)
    UPDATED_AT = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class FallComplianceEvent(Base):
    """Model representing fall compliance event records"""
    __tablename__ = 'fall_compliance_events'

    EVENT_ID = Column(Integer, primary_key=True)
    INCIDENT_ID = Column(Integer)  # ForeignKey can be added if needed
    NAME = Column(String)
    DATE = Column(DateTime)
    TIME = Column(String)
    EVENT_TYPE = Column(String)
    EVENT_SEQUENCE = Column(Integer)
    SCHEDULED_TIMESTAMP = Column(DateTime)
    ACTUAL_TIMESTAMP = Column(DateTime)
    EVENT_STATUS = Column(String)
    EVENT_DETAILS = Column(Text)
    NURSENAME = Column(String)
    CREATED_AT = Column(DateTime, default=datetime.utcnow)
