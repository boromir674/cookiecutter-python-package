import typing as t

__all__ = ['create_context']


def create_context(
    interpreters: t.Optional[t.Mapping[str, t.Sequence[str]]],
    extra_context: t.Optional[t.Mapping[str, t.Any]] = None,
) -> t.Mapping[str, t.Any]:
    if extra_context:
        return dict(
            extra_context,
            **{
                'interpreters': interpreters,
            }
        )
    return {
        'interpreters': interpreters,
    }
