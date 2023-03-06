variable "foo" {
  description = "String variable"
  type        = string
}

variable "bar" {
  description = "String variable with default"
  type        = number
}

variable "baz" {
  type        = list(string)
}

variable "qux" {
  description = "Boolean variable"
  default     = true
  type        = bool
}
