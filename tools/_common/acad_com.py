"""
Shared AutoCAD COM connection helper.

Attaches to the running AutoCAD instance via pywin32 and returns the
application and active document. Raises typed errors so callers can report
exactly what went wrong.

Project: Miller-Sweeney (AutoCAD 2023 target). Windows only.

Usage:
    from _common.acad_com import connect, AcadError, point
    acad, doc = connect()
"""

from __future__ import annotations

TARGET_MAJOR_VERSION = "24.2"  # AutoCAD 2023 reports acad.Version starting "24.2"


class AcadError(RuntimeError):
    """Base class. `code` is a short machine-readable tag, `fix` is user guidance."""

    code = "COM_ERROR"
    fix = (
        "Try: (1) restart AutoCAD, (2) run AutoCAD as Administrator once to "
        "re-register COM, (3) repair the AutoCAD installation."
    )

    def __init__(self, message: str, fix: str | None = None):
        super().__init__(message)
        if fix is not None:
            self.fix = fix

    def to_dict(self) -> dict:
        return {"status": "error", "code": self.code, "message": str(self), "fix": self.fix}


class NoPywin32(AcadError):
    code = "NO_PYWIN32"
    fix = "Run:  .venv\\Scripts\\pip install pywin32  then  python .venv\\Scripts\\pywin32_postinstall.py -install"


class NotRunning(AcadError):
    code = "NOT_RUNNING"
    fix = "Open AutoCAD 2023 and open a drawing (.dwg), then try again."


class NotInstalled(AcadError):
    code = "NOT_INSTALLED"
    fix = "Install AutoCAD 2023 for Windows. AutoCAD for Mac and AutoCAD Web do not support COM."


class NoDocument(AcadError):
    code = "NO_DOCUMENT"
    fix = "Open or create a .dwg file in AutoCAD, then try again."


class ReadOnly(AcadError):
    code = "READONLY"
    fix = (
        "Make sure the drawing is not opened read-only, not checked out by "
        "another user, and not in a non-editable state (e.g. Print Preview)."
    )


class WrongVersion(AcadError):
    code = "WRONG_VERSION"
    fix = "Close other AutoCAD releases and open the drawing in AutoCAD 2023."


def _autocad_installed() -> bool:
    import winreg

    for hive in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
        try:
            winreg.OpenKey(hive, r"SOFTWARE\Autodesk\AutoCAD")
            return True
        except FileNotFoundError:
            continue
    return False


def connect(require_document: bool = True, require_version: bool = False):
    """Attach to running AutoCAD. Returns (acad, doc); doc is None if not required and absent."""
    try:
        import win32com.client  # noqa: F401
        import pywintypes
    except ImportError as e:
        raise NoPywin32("pywin32 is not installed in the active Python.") from e

    try:
        acad = win32com.client.GetActiveObject("AutoCAD.Application")
    except pywintypes.com_error as e:
        if _autocad_installed():
            raise NotRunning("AutoCAD is installed but not running.") from e
        raise NotInstalled("AutoCAD does not appear to be installed on this computer.") from e
    except Exception as e:  # noqa: BLE001 — surface any other COM failure with guidance
        raise AcadError(f"COM error when connecting: {e}") from e

    if require_version:
        try:
            version = str(acad.Version)
        except Exception as e:  # noqa: BLE001
            raise AcadError(f"Could not read AutoCAD version: {e}") from e
        if not version.startswith(TARGET_MAJOR_VERSION):
            raise WrongVersion(
                f"Connected to AutoCAD version {version}; this project targets AutoCAD 2023 "
                f"(version {TARGET_MAJOR_VERSION}.x)."
            )

    doc = None
    try:
        doc = acad.ActiveDocument
        if doc is not None:
            _ = doc.Name
    except Exception:  # noqa: BLE001
        doc = None
    if doc is None and require_document:
        raise NoDocument("AutoCAD is running but no drawing is open.")
    return acad, doc


def point(x: float, y: float, z: float = 0.0):
    """Build a COM-safe 3D point array (VT_ARRAY of doubles)."""
    import pythoncom
    import win32com.client as wc

    return wc.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [float(x), float(y), float(z)])


def write_test(doc) -> None:
    """Add and delete a point in model space to prove the drawing is writable."""
    try:
        obj = doc.ModelSpace.AddPoint(point(0, 0, 0))
        obj.Delete()
    except Exception as e:  # noqa: BLE001
        raise ReadOnly(f"AutoCAD is connected but the drawing is read-only or locked: {e}") from e


def version_info(acad) -> dict:
    try:
        return {"version": str(acad.Version), "product": str(acad.Caption)}
    except Exception:  # noqa: BLE001
        return {"version": "unknown", "product": "AutoCAD"}
