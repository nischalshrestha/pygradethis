"""
This module is used to check python code output.
"""

import sys
from typing import Any, Union, List, Tuple

from .conditions import GraderCondition

def python_compare_output(user_output: Any, expected_output: Any) -> bool:
  """Return whether the user output and expected output match"""
  if type(user_output) != type(expected_output):
    return False
  # TODO: add more pandas + numpy DS
  # TODO this is okay for now and doesn't break existing functionality
  # but we will likely change this after refactoring checks to use asserts
  elif user_output.__class__.__name__ == "DataFrame" and expected_output.__class__.__name__ == "DataFrame":
    if "pandas" in sys.modules:
      return user_output.equals(expected_output)
    # we will want to properly handle this case in the future by raising Exception
    # when refactoring to the assertEqual approach this will become easier
    return False
  else:
    return user_output == expected_output
  
def python_grade_conditions(*conditions: GraderCondition, user_result: Any = None, r: dict = {}) -> Tuple[bool, GraderCondition]:
  """Goes through all conditions (python_pass_if, python_fail_if) and
  returns the first condition that comes True.

  Parameters
  ----------
  conditions : List[GraderCondition]
      
  user_result : Any
      [description]

  Returns
  -------
  Tuple[bool, GraderCondition]
      bool is True if user_result is correct, else False
      GraderCondition that matched with the user_result
  """
  # TODO handle the case where you might only have fail_ifs but they don't match (issue #4)
  result, condition = False,  None
  for cond in conditions:
    condition = cond
    result = python_compare_output(cond['x'], user_result)
    if result:
      return result, condition
  # If there is at least one pass_if() condition, then default to an incorrect grade;
  # otherwise, we default to a correct grade https://github.com/rstudio-education/gradethis/issues/118
  if len([c for c in conditions if c['correct']]) != 0:
    return False, None
  # otherwise if we only have fail_ifs, we default to a correct grade 
  # see https://github.com/rstudio-education/gradethis/issues/118
  elif len([c for c in conditions if not c['correct']]) != 0:
    return True, None
  return False, None

# TODO add the other kwargs for this?
# glue_correct = getOption("gradethis_glue_correct"),
# glue_incorrect = getOption("gradethis_glue_incorrect")
def python_grade_result(*conditions: List[GraderCondition], user_result: Any = None) -> Union[dict, str]:
  """This function checks the user's code output against the list of conditions.

  Parameters
  ----------
  conditions: *GraderCondition
      a variable number of GraderCondition objects
  user_result : Any, optional
      user's code output, by default None

  Returns
  -------
  Union[dict, str]
      dict, if there are no issues
      str, an error message if GraderCondition(s) is not supplied

  Raises
  ------
  Exception
      if GraderConditions are not passed in for conditions
  """
  all_conditions = [c for c in conditions if isinstance(c, GraderCondition)]
  if conditions == None or len(all_conditions) == 0:
    raise Exception(
      "At least one condition object (e.g., `python_pass_if()`, "
      "`python_fail_if()`, `python_condition()`) must be provided to"
      "`python_grade_result()`"
    )
  if user_result is not None:
    return python_grade_conditions(*conditions, user_result=user_result)
  return conditions

if __name__ != '__main__':
  try:
    # attempt to import `pandas`
    import pandas
  except:
    pass
