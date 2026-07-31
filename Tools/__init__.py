try:
	from .visual_navigation import navigate_visually
except Exception:
	# Provide a lightweight fallback so the package can be imported
	# in environments where `crewai` or other optional deps are missing.
	def navigate_visually(*args, **kwargs):
		raise RuntimeError(
			"visual navigation tool unavailable: install optional deps from requirements.txt to enable it"
		)

__all__ = ["navigate_visually"]