from enum import Enum

# NOTE: We will be removing the translation when we have the i18n in place
FSM_STATE_TRANSLATION = {
    'new': { 
        'label_es': 'Nuevo Registro',
        'label_en': 'New Record',
    },
    'submitted': {
        'label_es': 'Enviado',
        'label_en': 'Submitted',
    },
    'in_evaluation_by_DCC': {
        'label_es': 'En Evaluación por DCC',
        'label_en': 'In Evaluation by DCC',
    },
    'requested_changes_by_DCC': {
        'label_es': 'Solicitud de Cambios por DCC',
        'label_en': 'Requested Changes by DCC',
    },
    'updating_by_request_DCC': {
        'label_es': 'Actualización del Registro por Solicitud de la DCC',
        'label_en': 'Updating the Record by Request of the DCC',
    },
    'accepted_by_DCC': {
        'label_es': 'Aceptado por DCC',
        'label_en': 'Accepted by DCC',
    },
    'rejected_by_DCC': {
        'label_es': 'Rechazado por DCC',
        'label_en': 'Rejected by DCC',
    },
    'registered_by_DCC': {
        'label_es': 'Registrado por DCC',
        'label_en': 'Registered by DCC',
    },
    'end': {
        'label_es': 'Finalizado',
        'label_en': 'Finished',
    },
}

class States(str, Enum):
    NEW = 'new'
    SUBMITTED = 'submitted'
    IN_EVALUATION_BY_DCC = 'in_evaluation_by_DCC'
    REQUESTED_CHANGES_BY_DCC = 'requested_changes_by_DCC'
    UPDATING_BY_REQUEST_DCC = 'updating_by_request_DCC'
    ACCEPTED_BY_DCC = 'accepted_by_DCC'
    REJECTED_BY_DCC = 'rejected_by_DCC'
    REGISTERED_BY_DCC = 'registered_by_DCC'
    END = 'end'

