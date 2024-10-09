# from sqlalchemy.orm import Session
# from docs_maker.database.models import Configurations


class ServiceConfigurations:
    # @staticmethod
    # def insert_or_update_config(session: Session, config_key: str, config_value: str):
    #     existing_config = session.query(Configurations).filter_by(config_key=config_key).first()
    #
    #     if existing_config:
    #         existing_config.config_value = config_value
    #         session.commit()
    #         return existing_config
    #     else:
    #         new_config = Configurations(config_key=config_key, config_value=config_value)
    #         session.add(new_config)
    #         session.commit()
    #         # session.refresh(new_config)
    #         return new_config
    pass
