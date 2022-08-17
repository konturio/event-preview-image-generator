from typing import Dict
from dataclasses import dataclass, fields, replace, asdict
from starlette.config import Config


@dataclass
class Secret:
    CACHE_PASSWORD: str = None

    def __post_init__(self):
        config = Config('../.env')
        for field in fields(self):
            value = getattr(self, field.name)
            if value == field.default:
                setattr(self, field.name, config(field.name, cast=field.type, default=field.default))
            elif not isinstance(value, field.type):
                setattr(self, field.name, field.type(value))

    def copy(self) -> 'Secret':
        return replace(self)

    def asdict(self) -> Dict[str, str]:
        return {key: str(value) for key, value in asdict(self).items()}