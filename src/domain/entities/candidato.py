from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class Candidato:
    urn_id: str
    nome: str
    cargo: str
    perfil_url: str
    access_token: str
    data_cadastro: datetime
    ativo: bool = True

    def esta_expirado(self) -> bool:
        return datetime.now() > self.data_cadastro + timedelta(days=30)

    @classmethod
    def from_dict(cls, data: dict):
        data['data_cadastro'] = datetime.fromisoformat(data['data_cadastro'])
        return cls(**data)

    def to_dict(self) -> dict:
        data = self.__dict__.copy()
        data['data_cadastro'] = self.data_cadastro.isoformat()
        return data