from enum import Enum


class Asset(Enum):
    ACTIVE = "A"
    ACTIVE_HIGH = "AH"
    FROZEN = "F"
    FROZEN_HIGH = "FH"
    UNKNOWN = "U"


class Job(Enum):
    QUEUED = "JQ"
    RUNNING = "JR"
    FAIL = "JF"
    PASS = "JP"


class Risk(Enum):
    TRIAGE_INFO = "TI"
    TRIAGE_LOW = "TL"
    TRIAGE_MEDIUM = "TM"
    TRIAGE_HIGH = "TH"
    TRIAGE_CRITICAL = "TC"
    OPEN_INFO = "OI"
    OPEN_LOW = "OL"
    OPEN_MEDIUM = "OM"
    OPEN_HIGH = "OH"
    OPEN_CRITICAL = "OC"
    CLOSED_INFO = "CI"
    CLOSED_LOW = "CL"
    CLOSED_MEDIUM = "CM"
    CLOSED_HIGH = "CH"
    CLOSED_CRITICAL = "CC"
    CLOSED_INFO_ACCEPTED = "CIA"
    CLOSED_LOW_ACCEPTED = "CLA"
    CLOSED_MEDIUM_ACCEPTED = "CMA"
    CLOSED_HIGH_ACCEPTED = "CHA"
    CLOSED_CRITICAL_ACCEPTED = "CCA"
    CLOSED_INFO_REJECTED = "CIR"
    CLOSED_LOW_REJECTED = "CLR"
    CLOSED_MEDIUM_REJECTED = "CMR"
    CLOSED_HIGH_REJECTED = "CHR"
    CLOSED_CRITICAL_REJECTED = "CCR"


Status = {'asset': Asset, 'seed': Asset, 'job': Job, 'risk': Risk}
