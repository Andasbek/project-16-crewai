import inspect
import crew
print(f"crew module file: {crew.__file__}")
from crew import build_crew
print(f"build_crew signature: {inspect.signature(build_crew)}")
