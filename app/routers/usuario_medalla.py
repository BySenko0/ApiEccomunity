from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.medalla import UsuarioMedalla, Medalla
from app.schemas.usuario_medalla import UsuarioMedallaCreate, UsuarioMedallaOut
from app.schemas.medalla import MedallaOut

router = APIRouter(prefix="/usuarios-medallas", tags=["Usuarios - Medallas"])

# 🏅 Asignar medalla a un usuario
@router.post("/", response_model=UsuarioMedallaOut)
async def asignar_medalla(data: UsuarioMedallaCreate, db: AsyncSession = Depends(get_db)):
    # Validar si ya tiene esa medalla
    result = await db.execute(
        select(UsuarioMedalla).where(
            UsuarioMedalla.id_usuario == data.id_usuario,
            UsuarioMedalla.id_medalla == data.id_medalla
        )
    )
    if result.scalar():
        raise HTTPException(status_code=400, detail="El usuario ya tiene esta medalla.")

    nueva = UsuarioMedalla(**data.dict())
    db.add(nueva)
    await db.commit()
    await db.refresh(nueva)
    return nueva

# 🧾 Obtener todas las medallas asignadas a un usuario (solo relaciones)
@router.get("/usuario/{id_usuario}", response_model=list[UsuarioMedallaOut])
async def obtener_medallas_usuario(id_usuario: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(UsuarioMedalla).where(UsuarioMedalla.id_usuario == id_usuario)
    )
    return result.scalars().all()

# 🧾 Obtener detalles completos de medallas de un usuario
@router.get("/usuario/{id_usuario}/detalle", response_model=list[MedallaOut])
async def obtener_medallas_completas_usuario(id_usuario: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Medalla).join(UsuarioMedalla).where(UsuarioMedalla.id_usuario == id_usuario)
    )
    return result.scalars().all()
