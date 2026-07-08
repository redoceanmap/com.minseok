from fastapi import Depends

from sherlock_homes.adapter.outbound.gateways.detective_spam_classifier_gateway import ExaoneSpamClassifierGateway
from sherlock_homes.app.ports.input.detective_spam_classifier_use_case import SpamClassifierUseCase
from sherlock_homes.app.ports.output.detective_spam_classifier_port import SpamClassifierPort
from sherlock_homes.app.use_cases.detective_spam_classifier_interactor import SpamClassifierInteractor


def get_spam_classifier_repository() -> SpamClassifierPort:
    return ExaoneSpamClassifierGateway()


def get_spam_classifier_use_case(
    repository: SpamClassifierPort = Depends(get_spam_classifier_repository),
) -> SpamClassifierUseCase:
    return SpamClassifierInteractor(port=repository)
