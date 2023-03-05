variable "string_var" {
  description = "String variable"
  type        = string
}

variable "string_var_w_default" {
  description = "String variable with default"
  type        = string
  default     = "default"
}

variable "string_var_wo_description" {
  type        = string
}

variable "bool_var" {
  description = "Boolean variable"
  type        = bool
}

variable "bool_var_w_default" {
  description = "Boolean variable"
  default     = true
  type        = bool
}

variable "list_string" {
  description = "List of strings"
  type        = list(string)
}

variable "list_string_w_default" {
  description = "List of strings"
  type        = list(string)
  default     = ["test"]
}

variable "algorithm" {
  description = "linear or seasonal"
  type        = string
  default     = "seasonal"
  validation {
    condition     = var.algorithm == "seasonal" || var.algorithm == "linear"
    error_message = "Var algorithm must be seasonal or linear."
  }
}

variable "deviations" {
  description = "A number greater than or equal to one. This parameter controls the size of the confidence bounds, allowing a monitor to be made more or less sensitive."
  type        = number
  default     = 1
  validation {
    condition     = var.deviations >= 1
    error_message = "Var deviations must be >= 1."
  }
}

variable "map" {
  description = "map"
  type        = map(string)
}

variable "map_w_default" {
  description = "map"
  default     = {}
  type        = map(string)
}
