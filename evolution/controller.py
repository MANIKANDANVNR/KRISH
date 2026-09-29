from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


@dataclass
class EvolutionProposal:

    proposal_id: str

    target: str

    reason: str

    changes: list[str]

    risk: str

    approved: bool = False

    created_at: datetime = field(
        default_factory=lambda:
            datetime.now(timezone.utc)
    )


class EvolutionController:

    MODE = "observe_only"

    def __init__(self):

        self.proposals = {}

    def observe(
        self,
        target,
        observation,
    ):

        return {
            "target": target,
            "observation": observation,
            "mode": self.MODE,
        }

    def propose(
        self,
        target,
        reason,
        changes,
        risk="high",
    ):

        proposal = EvolutionProposal(
            proposal_id=str(uuid4()),
            target=target,
            reason=reason,
            changes=list(changes),
            risk=risk,
        )

        self.proposals[
            proposal.proposal_id
        ] = proposal

        return proposal

    def approve(
        self,
        proposal_id,
    ):

        proposal = self.proposals.get(
            proposal_id
        )

        if proposal is None:
            raise KeyError(
                "Unknown evolution proposal."
            )

        proposal.approved = True

    def modify(self, *args, **kwargs):

        raise PermissionError(
            "Direct self modification is disabled. "
            "Use the owner-approved evolution workflow."
        )