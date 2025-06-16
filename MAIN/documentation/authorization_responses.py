from schemas.authorization import GoogleCreatedUserResponse
RESPONSES = {
    "GET": {},
    "POST": {
        "/login": {
            200: {"description": "All good (user authorized, JWTs created)."},
            422: {"description": "Invalid user data."},
            401: {"description": "Incorrect `username` or `password` (`detail`: \"Incorrect username or password\")."},
            403: {"description": "`Email` not verified. (`detail`: \"Email not verified\")"}
        },
        "/google/auth/callback": { #no unit tests
            200: {"description": "Successful login (`detail`: \"Success\")."},
            201: {"model": GoogleCreatedUserResponse, "description": "Successful registration (`detail`: \"Success\")."},
            400: {"description": "Invalid token response from Google (`detail`: \"Invalid token\")."},
            422: {"description": "Invalid code."}
        },
        "/refresh": {
            200: {"description": "All good (new JWT access + refresh created)."},
            401: {"description": (
                    "Unauthorized access.\n\n"
                    "Possible reasons:\n"
                    "- **Reason 1**: The refresh token is expired (user should relogin) (`detail`: \"Expired token\").\n"
                    "- **Reason 2**: The refresh token is invalid (`detail`: \"Invalid token\").\n"
                    "- **Reason 3**: Missing `user_id` or `username` in the decoded token (`detail`: \"Invalid token\").\n"
                    " or `username` from token does not exist.\n"
                )
            },
            403: { "description":"Strange activity (rather compromised token) -> must relogin (`detail`: \"User must relogin\").\n"},
            422: {"description": "Invalid token."}
        },
        "/register": {
            201: {"description": "Successful registration."},
            422: {
                "description": (
                    "Validation error.\n\n"
                    "Possible reasons:\n"
                    "- **Invalid `username`**: `username` must be between 3 and 50 characters, and can only contain letters, numbers, and underscores.\n"
                    "- **Invalid email format**: `email` must be a valid email address.\n"
                    "- **Invalid `password`**: `password` must contain at least one uppercase letter, one lowercase letter, one number, and one special character.\n"
                    "- **Invalid `name`**: Name can only contain letters, hyphens, apostrophes, and spaces\n"
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
            409: {"description" : (
                    "Duplicate values. \n\n"
                    "Possible duplicates:\n"
                    "- **Duplicate 1**: `username` (`detail`: \"Username already exists\").\n"
                    "- **Duplicate 2**: `email` (`detail`: \"Email already exists\")."
                )
            }
        },
        "/verify-email-link" : {
            200: {"description": "Success. (`detail`: \"Success\").\n"},
            404: {"description": "User not found. (`detail`: \"User not found\").\n"},
            409: {"description": "The email has already been verified (`detail`: \"The email has already been verified\")."},
            422: {
                "description": "Invalid email.",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": [
                                {
                                    "type": "value_error",
                                    "loc": [
                                        "query",
                                        "email"
                                    ],
                                    "msg": "value is not a valid email address: An email address must have an @-sign.",
                                    "input": "ivan.ivanov21",
                                    "ctx": {
                                        "reason": "An email address must have an @-sign."
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        },
        "/verify-email": {
            200: {
                "description": "Success. (`detail`: \"Success\")"
            },
            401: {
                "description": (
                    "Verification failed.\n\n"
                    "Possible reasons:\n"
                    "- **Expired token**: The verification link has expired (`detail`: \"Expired token\").\n"
                    "- **Invalid token**: The verification link is incorrect or has been tampered with (`detail`: \"Invalid token\")."
                    "- **Invalid email**: Email string doesn't look like emailstr (`detail`: \"Invalid email\")."
                ),
                "content": {
                    "application/json": {
                        "examples": [
                            {"detail": "Invalid token"},
                            {"detail": "Exired token"}
                        ]
                    }
                }
            },
            404: {"description": "User not found (`detail`: \"User not found\")."},
            409: {"description": "The email has already been verified (`detail`: \"The email has already been verified\")."}
        },
        "/forgot-password": {
            200: {"description": "`Password` reset link successfully sent to the user's email (`detail`: \"Success\")."},
            404: {
                "description": "`User` not found.",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": "`User` not found"
                        }
                    }
                }
            },
            422: {
                "description": "Invalid email address.",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": "Invalid email format"
                        }
                    }
                }
            }
        },
        "/logout": {
            200: {"description": "Success. (`detail`: \"Success\").\n"},
            401: {"description": (
                    "Unauthorized access.\n\n"
                    "Possible reasons:\n"
                    "- **Reason 1**: The `access token` is expired (should update `access token`) (`detail`: \"Expired token\").\n"
                    "- **Reason 2**: The `access token` is invalid (`detail`: \"Invalid token\").\n"
                    "- **Reason 3**: Missing `user_id` or `username` in the decoded token (`detail`: \"Invalid token\").\n"
                    " or `username` from token does not exist.\n"
                )
            },
            403: { "description": (
                    "Forbidden.\n\n"
                    "Possible reasons:\n"
                    "- **Reason 1**: Strange activity (rather compromised token) -> must relogin (`detail`: \"User must relogin\").\n"
                    "- **Reason 2**: Missing header Authorization with Bearer `access token` (`detail`: \"Not authenticated\").\n"
                )  
            }
        }
    },
    "PUT": {
        "/password-forgot": {
            200: {"description": "`Password` successfully reset (`detail`: \"Success\")."},
            403: {"description": "Email not verified (`detail`: \"Email not verified\")."},
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
                                    "msg": "Username can only contain letters, numbers, and underscores",
                                    "type": "value_error"
                                }
                            ]
                        }
                    }
                }
            },
            401: {
                "description": (
                    "Token errors.\n\n"
                    "Possible `details`:\n"
                    "- **Invalid token**.\n"
                    "- **Expired token**.\n"
                    "- **Already used token**.\n"
                ),
                "content": {
                    "application/json": {
                        "examples": [
                            {"detail": "Invalid token"},
                            {"detail": "Exired token"},
                            {"detail": "Already used token"}
                        ]
                    }
                }
            },
            404: {
                "description": "`Email` not found",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": "Email not found"
                        }
                    }
                }
            },
            409: {
                "description": "New `password` must be different from the old one.",
                "content": {
                    "application/json": {
                        "example": {
                            "detail": "New password must be different from the old one."
                        }
                    }
                }
            }
        }
    },
    "DELETE": {}
}