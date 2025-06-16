DEFAULT_AUTH_RESPONSES = {
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

DEFAULT_OTP_AUTH_RESPONSES = {
    401: {"description": (
            "Unauthorized access.\n\n"
            "Possible reasons:\n"
            "- **Reason 1**: The `access token` is expired (should update `access token`) (`detail`: \"Expired token\").\n"
            "- **Reason 2**: The `access token` is invalid (`detail`: \"Invalid token\").\n"
            "- **Reason 3**: Missing `user_id` or `username` in the decoded token (`detail`: \"Invalid token\").\n"
            " or `username` from token does not exist.\n"
            "- **Reason 4**: OTP expired or invalid (`detail`: \"OTP expired or invalid\").\n"
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

DEFAULT_OPTIONAL_AUTH_RESPONSES = {
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
        )  
    }
}