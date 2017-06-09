variable "region"{
}
variable "count"{
}
variable "subnet_id"{
}
variable "sg_id"{
}

variable "ami_id" {
  type = "map"
  default = {
    "us-east-1" = "ami-6d1c2007"
    "us-east-2" = "ami-6a2d760f"
    "ap-southeast-1" = "ami-f068a193"
    "ap-southeast-2" = "ami-fedafc9d"
    "us-west-1" = "ami-af4333cf"
    "us-west-2" = "ami-d2c924b2"
  }
}

variable "key"{
	default = "ms_treadmill_dev"
}

variable "size" {
  type = "map"
  default = {
    "freeipa" = "t2.micro"
  }
}
variable "role"{
}
