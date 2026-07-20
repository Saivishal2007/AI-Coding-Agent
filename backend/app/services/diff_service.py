import difflib

from app.core.logging import get_logger

logger = get_logger(__name__)


class DiffService:
    """
    Generates unified diffs and diff statistics.
    """

    @staticmethod
    def generate(
        old_content: str,
        new_content: str,
    ) -> str:

        diff = difflib.unified_diff(
            old_content.splitlines(),
            new_content.splitlines(),
            fromfile="old",
            tofile="new",
            lineterm="",
        )

        return "\n".join(diff)

    @staticmethod
    def statistics(
        old_content: str,
        new_content: str,
    ) -> dict:

        old_lines = old_content.splitlines()

        new_lines = new_content.splitlines()

        matcher = difflib.SequenceMatcher(
            None,
            old_lines,
            new_lines,
        )

        added = 0
        removed = 0
        changed = 0

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():

            if tag == "insert":

                added += (j2 - j1)

            elif tag == "delete":

                removed += (i2 - i1)

            elif tag == "replace":

                changed += max(
                    i2 - i1,
                    j2 - j1,
                )

        logger.info(
            "Diff Statistics -> Added: %d | Removed: %d | Changed: %d",
            added,
            removed,
            changed,
        )

        return {
            "added": added,
            "removed": removed,
            "changed": changed,
            "total": added + removed + changed,
        }