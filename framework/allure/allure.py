from enum import StrEnum


class AllureParentSuite(StrEnum):
    ADVERTISEMENTS = "Advertisements statistics service"


class AllureSuite(StrEnum):
    ADVERTISEMENTS = "Advertisements"


class AllureSubSuite(StrEnum):
    GET_ENTITY = "Get entity"
    GET_ENTITIES = "Get entities"
    CREATE_ENTITY = "Create entity"
    DELETE_ENTITY = "Delete entity"


class AllureTag(StrEnum):
    SMOKE = "SMOKE"
    FUNCTION = "FUNCTION"
    E2E = "E2E"
    REGRESSION = "REGRESSION"
    HAPPY_PASS = "HAPPY_PASS"
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"

    GET_ENTITY = "GET_ENTITY"
    GET_ENTITIES = "GET_ENTITIES"
    CREATE_ENTITY = "CREATE_ENTITY"
    DELETE_ENTITY = "DELETE_ENTITY"
