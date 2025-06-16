RESPONSES = {
    "GET": {
        "/my-active-sessions": {
            200: {"description": "Success."},
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
    "POST": {},
    "PUT": {},
    "DELETE": {
            "/session": {
            200: {"description": "Success (`detail`: \"Success\").\n"},
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
                    "- **Reason 3**: Session does not belong to user (`detail`: \"Session does not belong to the authenticated user\").\n"
                )  
            },
            409: {"description": "This session is current, can't logout this way (`detail`: \"Can't logout user's session this way\")."}
        },
        "/sessions": {
            200: {"description": "Success (`detail`: \"Success\").\n"},
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
    }
}