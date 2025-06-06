# Based on pydantic-settings version 0.2.5 by Daniel Daniels, licensed under MIT
#
# See <https://github.com/danields761/pydantic-settings>

from typing import Type

from .class_doc import extract_docs_from_cls_obj
from pydantic import BaseModel
from pydantic import __version__ as pydantic_version

if pydantic_version.startswith("1."):
    # pydantic 1.x
    def apply_attributes_docs(
        model: Type[BaseModel], override_existing: bool = True
    ) -> None:
        """
        Apply model attributes documentation in-place. Resulted docs are placed
        inside :code:`field.schema.description` for *pydantic* model field.
        :param model: any pydantic model
        :param override_existing: override existing descriptions
        """
        docs = extract_docs_from_cls_obj(model)

        for field in model.__fields__.values():
            if field.field_info.description and not override_existing:
                continue

            try:
                field.field_info.description = '\n'.join(docs[field.name])
            except KeyError:
                pass

else:
    # pydantic 2.x
    import pydantic.v1 as pydantic_v1
    del pydantic_v1

    def apply_attributes_docs(
        model: Type[BaseModel], override_existing: bool = True
    ) -> None:
        """
        Apply model attributes documentation in-place. Resulted docs are placed
        inside :code:`field.schema.description` for *pydantic* model field.
        :param model: any pydantic model
        :param override_existing: override existing descriptions
        """
        docs = extract_docs_from_cls_obj(model)

        for name, field in model.model_fields.items():
            if field.description and not override_existing:
                continue

            try:
                field.description = '\n'.join(docs[name])
            except KeyError:
                pass

def with_attrs_docs(
    model_cls: Type[BaseModel]
) -> Type[BaseModel]:
    """
    Applies :py:func:`.apply_attributes_docs`.
    """

    def decorator(maybe_model_cls: Type[BaseModel]) -> Type[BaseModel]:
        apply_attributes_docs(
            maybe_model_cls
        )
        return maybe_model_cls

    return decorator(model_cls)
