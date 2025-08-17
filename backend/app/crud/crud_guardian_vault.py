import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.encryption import decrypt, encrypt
from app.models.guardian_vault import GuardianVault
from app.schemas.guardian_vault import GuardianVaultCreate


async def get(db: AsyncSession, *, user_id: int) -> GuardianVault | None:
    result = await db.execute(
        select(GuardianVault).filter(GuardianVault.user_id == user_id)
    )
    vault = result.scalars().first()
    if vault:
        decrypted_data = decrypt(vault.encrypted_data)
        vault_data = json.loads(decrypted_data)
        return vault_data
    return None


async def create_or_update(
    db: AsyncSession, *, obj_in: GuardianVaultCreate, user_id: int
) -> GuardianVault:
    result = await db.execute(
        select(GuardianVault).filter(GuardianVault.user_id == user_id)
    )
    db_obj = result.scalars().first()

    data_to_encrypt = obj_in.model_dump_json()
    encrypted_data = encrypt(data_to_encrypt)

    if db_obj:
        db_obj.encrypted_data = encrypted_data
    else:
        db_obj = GuardianVault(user_id=user_id, encrypted_data=encrypted_data)

    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
