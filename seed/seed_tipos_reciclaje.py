from app.models.tipo_reciclaje import TipoReciclaje
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

async def seed_tipos_reciclaje(session: AsyncSession):
    tipos = [
        {
            "Nombre": "Plástico",
            "PesoMinimo": 0.5,
            "PesoMaximo": 50.0,
            "PagoPorKg": 2.0,
            "GananciaPorKg": 1.5,
        },
        {
            "Nombre": "Papel",
            "PesoMinimo": 1.0,
            "PesoMaximo": 100.0,
            "PagoPorKg": 1.0,
            "GananciaPorKg": 0.7,
        },
        {
            "Nombre": "Vidrio",
            "PesoMinimo": 2.0,
            "PesoMaximo": 80.0,
            "PagoPorKg": 1.5,
            "GananciaPorKg": 1.0,
        },
        {
            "Nombre": "Metal",
            "PesoMinimo": 0.2,
            "PesoMaximo": 60.0,
            "PagoPorKg": 3.0,
            "GananciaPorKg": 2.3,
        },
        {
            "Nombre": "Cartón",
            "PesoMinimo": 1.0,
            "PesoMaximo": 90.0,
            "PagoPorKg": 0.8,
            "GananciaPorKg": 0.5,
        },
        {
            "Nombre": "Electrónicos",
            "PesoMinimo": 0.1,
            "PesoMaximo": 30.0,
            "PagoPorKg": 5.0,
            "GananciaPorKg": 3.5,
        },
        {
            "Nombre": "Baterías",
            "PesoMinimo": 0.05,
            "PesoMaximo": 10.0,
            "PagoPorKg": 4.5,
            "GananciaPorKg": 2.0,
        },
        {
            "Nombre": "Textiles",
            "PesoMinimo": 0.5,
            "PesoMaximo": 70.0,
            "PagoPorKg": 1.2,
            "GananciaPorKg": 0.9,
        },
        {
            "Nombre": "Aceite usado",
            "PesoMinimo": 0.5,
            "PesoMaximo": 25.0,
            "PagoPorKg": 3.0,
            "GananciaPorKg": 2.0,
        },
        {
            "Nombre": "Madera",
            "PesoMinimo": 2.0,
            "PesoMaximo": 100.0,
            "PagoPorKg": 0.6,
            "GananciaPorKg": 0.4,
        },
        {
            "Nombre": "Llantas",
            "PesoMinimo": 5.0,
            "PesoMaximo": 150.0,
            "PagoPorKg": 2.8,
            "GananciaPorKg": 1.8,
        },
        {
            "Nombre": "Residuos orgánicos",
            "PesoMinimo": 1.0,
            "PesoMaximo": 100.0,
            "PagoPorKg": 0.4,
            "GananciaPorKg": 0.2,
        }
    ]


    for tipo in tipos:
        result = await session.execute(select(TipoReciclaje).where(TipoReciclaje.Nombre == tipo["Nombre"]))
        existente = result.scalar_one_or_none()

        if not existente:
            nuevo_tipo = TipoReciclaje(
                Nombre=tipo["Nombre"],
                PesoMinimo=tipo["PesoMinimo"],
                PesoMaximo=tipo["PesoMaximo"],
                PagoPorKg=tipo["PagoPorKg"],
                GananciaPorKg=tipo["GananciaPorKg"],
                FechaCreacion=date.today()
            )
            session.add(nuevo_tipo)
            print(f"♻️ Tipo de reciclaje '{tipo['Nombre']}' creado.")
        else:
            print(f"♻️ Tipo de reciclaje '{tipo['Nombre']}' ya existe.")

    await session.commit()
