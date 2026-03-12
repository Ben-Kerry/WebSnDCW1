from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.squad_membership import SquadMembershipCreate, SquadMembershipRead, SquadMembershipUpdate
from app.services.squad_membership import SquadMembershipService
from app.utils.responses import success_response

router = APIRouter(prefix="/squad-memberships", tags=["Squad Memberships"])


@router.get("", response_model=dict)
def list_memberships(db: Session = Depends(get_db)):
    data = [SquadMembershipRead.model_validate(item).model_dump() for item in SquadMembershipService(db).list_memberships()]
    return success_response(data, "Squad memberships retrieved")


@router.get("/{membership_id}", response_model=dict)
def get_membership(membership_id: int, db: Session = Depends(get_db)):
    membership = SquadMembershipService(db).get_membership(membership_id)
    return success_response(SquadMembershipRead.model_validate(membership).model_dump(), "Squad membership retrieved")


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_membership(payload: SquadMembershipCreate, db: Session = Depends(get_db)):
    membership = SquadMembershipService(db).create_membership(payload.model_dump())
    return success_response(SquadMembershipRead.model_validate(membership).model_dump(), "Squad membership created")


@router.put("/{membership_id}", response_model=dict)
def update_membership(membership_id: int, payload: SquadMembershipUpdate, db: Session = Depends(get_db)):
    membership = SquadMembershipService(db).update_membership(membership_id, payload.model_dump(exclude_unset=True))
    return success_response(SquadMembershipRead.model_validate(membership).model_dump(), "Squad membership updated")


@router.delete("/{membership_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_membership(membership_id: int, db: Session = Depends(get_db)):
    SquadMembershipService(db).delete_membership(membership_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)