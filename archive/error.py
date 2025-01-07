from datetime import datetime

def write_to_error_log(error_log_file,error, params):
  """Write error to error log"""
  with open(error_log_file, "a") as f:
    f.write(f"{datetime.now()} | {params} - {error}\n")