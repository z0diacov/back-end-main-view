from documentation.default_responses import DEFAULT_AUTH_RESPONSES

RESPONSES = {
    "GET": {
        "/me/has-password": {
            200: {"description": "Returns whether the current user has a password set."},
            **DEFAULT_AUTH_RESPONSES
        },
        "/trainer/profile": {
            200: {"description": "Returns trainer profile."},
            404: {
                "description": (
                    "Not Found.\n\n"
                    "Possible reasons:\n"
                    "- **User not found** (`detail`: \"User does not exist\").\n"
                    "- **Trainer profile not found** (`detail`: \"Trainer profile not found\")."
                )
            },
            422: {"description":  "Validation error: Invalid input parameters"}
        },
        "/user/profile": {
            200: {"description": "Returns user profile."},
            404: {"description": "User not found (`detail`: \"User does not exist\")."},
            422: {"description": "Validation error: Invalid input parameters"}
        },
        "/user/me/profile": {
            200: {"description": "Returns current user profile."},
            **DEFAULT_AUTH_RESPONSES
        },
        "/trainer/me/profile": {
            200: {"description": "Returns current user trainer profile."},
            403: {"description": "User is not a trainer (`detail`: \"User is not a trainer\")."},
            **DEFAULT_AUTH_RESPONSES
        }
    },
    "POST": {
        "/google/password/send": {
            200: {"description": "Email with OTP sent successfuly (`detail`: \"Success\")."},
            409: {"description": "User already has a password (`detail`: \"Password already exists\")"},
            **DEFAULT_AUTH_RESPONSES
        },
        "/google/password": {
            **DEFAULT_AUTH_RESPONSES,
            201: {"description": "Password successfuly added (`detail`: \"Success\")."},
            401: {
                "description": (
                    "Token errors.\n\n"
                    "Possible `details`:\n"
                    "- **Invalid token**.\n"
                    "- **Expired token**.\n"
                ),
                "content": {
                    "application/json": {
                        "examples": [
                            {"detail": "Invalid token"},
                            {"detail": "Exired token"},
                        ]
                    }
                }
            },
            409: {
                "description": (
                    "Possible reasons:\n"
                    "- **Password already exist.** (`detail`: \"Password already exist\").\n"
                    "- **User id from token (after pulling by email) does not equal id from auth** (`detail`: \"Token does not belong to current user\").\n"
                )
            }
        },
        "/trainer-profile": {
            **DEFAULT_AUTH_RESPONSES,
            201: {"description": "Trainer profile created successfuly (`detail`: \"Success\")."},
            409: {
                "description": "Trainer profile already exists.",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": "Trainer profile already exists"
                        }
                    }
                }
            },
            422: {
                "description": (
                    "Validation error.\n\n"
                    "- **Invalid `trainer_bio`**: `trainer_bio` must be at least 10 characters long and less than 4000.\n"
                    "All messages abount incorrect data will be given in `detail` in list where each element is object. Message - property \"msg\".\n"
                ),
                "content": {
                    "application/json": {
                        "example": {
                            "detail": [
                                {
                                    "loc": ["body", "trainer_bio"],
                                    "msg": "Trainer bio is too short",
                                    "type": "value_error"
                                }
                            ]
                        }
                    }
                }
            }
        }
    },
    "PUT": {
        "/username": {
            200: {"description": "Username changed successfuly (`detail`: \"Success\")."},
            401: {
                "description": "`OTP` expired or invalid ",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": "OTP expired or invalid "
                        }
                    }
                }
            },
            409: {
                "description": "New `username` already exists.",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": "New username already exists"
                        }
                    }
                }
            },
            422: {
                "description": (
                    "Validation error.\n\n"
                    "Possible reasons:\n"
                    "- **Invalid token**\n"
                    "- **Invalid `username`**: `username` must be between 3 and 50 characters, and can only contain letters, numbers, and underscores.\n"
                    "All messages abount incorrect data will be given in `detail` in list where each element is object. Message - property \"msg\".\n"
                ),
                "content": {
                    "application/json": {
                        "example": {
                            "detail": [
                                {
                                    "loc": ["body", "username"],
                                    "msg": "Username can only contain letters, numbers, and underscores",
                                    "type": "value_error"
                                }
                            ]
                        }
                    }
                }
            },
            **DEFAULT_AUTH_RESPONSES
        },
        "/password": {
            200: {"description": "Password changed successfuly (`detail`: \"Success\")."},
            400: {"description": "Incorrect old password (`detail`: \"Incorrect old password\")."},
            409: {
                "description": "New `password` must be different from the old one.",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": "New password must be different from the old one."
                        }
                    }
                }
            },
            422: {
                "description": (
                    "Validation error.\n\n"
                    "Possible reasons:\n"
                    "- **Invalid token**\n"
                    "- **Invalid `password`**: `password` must contain at least one uppercase letter, one lowercase letter, one number, and one special character.\n"
                    "All messages abount incorrect data will be given in `detail` in list where each element is object. Message - property \"msg\".\n"
                ),
                "content": {
                    "application/json": {
                        "example": {
                            "detail": [
                                {
                                    "loc": ["body", "username"],
                                    "msg": "Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character.",
                                    "type": "value_error"
                                }
                            ]
                        }
                    }
                }
            },
            **DEFAULT_AUTH_RESPONSES
        },
        "/email": {
            200: {"description": "Email changed successfuly (`detail`: \"Success\")."},
            401: {
                "description": "`OTP` expired or invalid ",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": "OTP expired or invalid "
                        }
                    }
                }
            },
            409: {
                "description": "New `email` already exists.",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": "New email already exists"
                        }
                    }
                }
            },
            422: {
                "description": (
                    "Validation error.\n\n"
                    "Possible reasons:\n"
                    "- **Invalid token**\n"
                    "- **Invalid email format**: `email` must be a valid email address.\n"
                    "All messages abount incorrect data will be given in `detail` in list where each element is object. Message - property \"msg\".\n"
                ),
                "content": {
                    "application/json": {
                        "example": {
                            "detail": [
                                {
                                    "loc": ["body", "username"],
                                    "msg": "Email must be a valid email address.",
                                    "type": "value_error"
                                }
                            ]
                        }
                    }
                }
            },
            **DEFAULT_AUTH_RESPONSES
        },
        "/name": {
            200: {"description": "Name changed successfuly (`detail`: \"Success\")."},
            409: {
                "description": "New `name` must be different from the old one.",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": "New name must be different from the old one"
                        }
                    }
                }
            },
            422: {
                "description": (
                    "Validation error.\n\n"
                    "Possible reasons:\n"
                    "- **Invalid token**\n"
                    "- **Invalid `name`**: Name can only contain letters, hyphens, apostrophes, and spaces\n"
                    "All messages abount incorrect data will be given in `detail` in list where each element is object. Message - property \"msg\".\n"
                ),
                "content": {
                    "application/json": {
                        "example": {
                            "detail": [
                                {
                                    "loc": ["body", "username"],
                                    "msg": "Name can only contain letters, hyphens, apostrophes, and spaces.",
                                    "type": "value_error"
                                }
                            ]
                        }
                    }
                }
            },
            **DEFAULT_AUTH_RESPONSES
        },
        "/profile-picture": {
            **DEFAULT_AUTH_RESPONSES
        },
        "/trainer-bio": {
            200: {"description": "Trainer bio changed successfuly (`detail`: \"Success\")."},
            403: {
                "description": "User does not have a trainer profile",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": "You must create a trainer profile before updating your bio"
                        }
                    }
                }
            },
            409: {
                "description": "New `trainer_bio` must be different from the old one.",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": "New trainer_bio must be different from the old one"
                        }
                    }
                }
            },
            422: {"description":  "Validation error: trainer_bio must be at least 10 characters long and less than 4000"},
            **DEFAULT_AUTH_RESPONSES
        }
    }
}