IDL_JSON = {
  "version": "0.1.0",
  "name": "jupiter",
  "instructions": [
    {
      "name": "route",
      "docs": [
        "route_plan Topologically sorted trade DAG"
      ],
      "accounts": [
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "userTransferAuthority",
          "isMut": False,
          "isSigner": True
        },
        {
          "name": "userSourceTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userDestinationTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "destinationTokenAccount",
          "isMut": True,
          "isSigner": False,
          "isOptional": True
        },
        {
          "name": "destinationMint",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "platformFeeAccount",
          "isMut": True,
          "isSigner": False,
          "isOptional": True
        },
        {
          "name": "eventAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "program",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": [
        {
          "name": "routePlan",
          "type": {
            "vec": {
              "defined": "RoutePlanStep"
            }
          }
        },
        {
          "name": "inAmount",
          "type": "u64"
        },
        {
          "name": "quotedOutAmount",
          "type": "u64"
        },
        {
          "name": "slippageBps",
          "type": "u16"
        },
        {
          "name": "platformFeeBps",
          "type": "u8"
        }
      ],
      "returns": "u64"
    },
    {
      "name": "routeWithTokenLedger",
      "accounts": [
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "userTransferAuthority",
          "isMut": False,
          "isSigner": True
        },
        {
          "name": "userSourceTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userDestinationTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "destinationTokenAccount",
          "isMut": True,
          "isSigner": False,
          "isOptional": True
        },
        {
          "name": "destinationMint",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "platformFeeAccount",
          "isMut": True,
          "isSigner": False,
          "isOptional": True
        },
        {
          "name": "tokenLedger",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "eventAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "program",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": [
        {
          "name": "routePlan",
          "type": {
            "vec": {
              "defined": "RoutePlanStep"
            }
          }
        },
        {
          "name": "quotedOutAmount",
          "type": "u64"
        },
        {
          "name": "slippageBps",
          "type": "u16"
        },
        {
          "name": "platformFeeBps",
          "type": "u8"
        }
      ],
      "returns": "u64"
    },
    {
      "name": "exactOutRoute",
      "accounts": [
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "userTransferAuthority",
          "isMut": False,
          "isSigner": True
        },
        {
          "name": "userSourceTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userDestinationTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "destinationTokenAccount",
          "isMut": True,
          "isSigner": False,
          "isOptional": True
        },
        {
          "name": "sourceMint",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "destinationMint",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "platformFeeAccount",
          "isMut": True,
          "isSigner": False,
          "isOptional": True
        },
        {
          "name": "token2022Program",
          "isMut": False,
          "isSigner": False,
          "isOptional": True
        },
        {
          "name": "eventAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "program",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": [
        {
          "name": "routePlan",
          "type": {
            "vec": {
              "defined": "RoutePlanStep"
            }
          }
        },
        {
          "name": "outAmount",
          "type": "u64"
        },
        {
          "name": "quotedInAmount",
          "type": "u64"
        },
        {
          "name": "slippageBps",
          "type": "u16"
        },
        {
          "name": "platformFeeBps",
          "type": "u8"
        }
      ],
      "returns": "u64"
    },
    {
      "name": "sharedAccountsRoute",
      "docs": [
        "Route by using program owned token accounts and open orders accounts."
      ],
      "accounts": [
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "programAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "userTransferAuthority",
          "isMut": False,
          "isSigner": True
        },
        {
          "name": "sourceTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "programSourceTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "programDestinationTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "destinationTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "sourceMint",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "destinationMint",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "platformFeeAccount",
          "isMut": True,
          "isSigner": False,
          "isOptional": True
        },
        {
          "name": "token2022Program",
          "isMut": False,
          "isSigner": False,
          "isOptional": True
        },
        {
          "name": "eventAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "program",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": [
        {
          "name": "id",
          "type": "u8"
        },
        {
          "name": "routePlan",
          "type": {
            "vec": {
              "defined": "RoutePlanStep"
            }
          }
        },
        {
          "name": "inAmount",
          "type": "u64"
        },
        {
          "name": "quotedOutAmount",
          "type": "u64"
        },
        {
          "name": "slippageBps",
          "type": "u16"
        },
        {
          "name": "platformFeeBps",
          "type": "u8"
        }
      ],
      "returns": "u64"
    },
    {
      "name": "sharedAccountsRouteWithTokenLedger",
      "accounts": [
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "programAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "userTransferAuthority",
          "isMut": False,
          "isSigner": True
        },
        {
          "name": "sourceTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "programSourceTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "programDestinationTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "destinationTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "sourceMint",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "destinationMint",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "platformFeeAccount",
          "isMut": True,
          "isSigner": False,
          "isOptional": True
        },
        {
          "name": "token2022Program",
          "isMut": False,
          "isSigner": False,
          "isOptional": True
        },
        {
          "name": "tokenLedger",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "eventAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "program",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": [
        {
          "name": "id",
          "type": "u8"
        },
        {
          "name": "routePlan",
          "type": {
            "vec": {
              "defined": "RoutePlanStep"
            }
          }
        },
        {
          "name": "quotedOutAmount",
          "type": "u64"
        },
        {
          "name": "slippageBps",
          "type": "u16"
        },
        {
          "name": "platformFeeBps",
          "type": "u8"
        }
      ],
      "returns": "u64"
    },
    {
      "name": "sharedAccountsExactOutRoute",
      "docs": [
        "Route by using program owned token accounts and open orders accounts."
      ],
      "accounts": [
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "programAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "userTransferAuthority",
          "isMut": False,
          "isSigner": True
        },
        {
          "name": "sourceTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "programSourceTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "programDestinationTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "destinationTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "sourceMint",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "destinationMint",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "platformFeeAccount",
          "isMut": True,
          "isSigner": False,
          "isOptional": True
        },
        {
          "name": "token2022Program",
          "isMut": False,
          "isSigner": False,
          "isOptional": True
        },
        {
          "name": "eventAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "program",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": [
        {
          "name": "id",
          "type": "u8"
        },
        {
          "name": "routePlan",
          "type": {
            "vec": {
              "defined": "RoutePlanStep"
            }
          }
        },
        {
          "name": "outAmount",
          "type": "u64"
        },
        {
          "name": "quotedInAmount",
          "type": "u64"
        },
        {
          "name": "slippageBps",
          "type": "u16"
        },
        {
          "name": "platformFeeBps",
          "type": "u8"
        }
      ],
      "returns": "u64"
    },
    {
      "name": "setTokenLedger",
      "accounts": [
        {
          "name": "tokenLedger",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenAccount",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "createOpenOrders",
      "accounts": [
        {
          "name": "openOrders",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "payer",
          "isMut": True,
          "isSigner": True
        },
        {
          "name": "dexProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "systemProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "rent",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "market",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "createTokenAccount",
      "accounts": [
        {
          "name": "tokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "user",
          "isMut": True,
          "isSigner": True
        },
        {
          "name": "mint",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "systemProgram",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": [
        {
          "name": "bump",
          "type": "u8"
        }
      ]
    },
    {
      "name": "createProgramOpenOrders",
      "accounts": [
        {
          "name": "openOrders",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "payer",
          "isMut": True,
          "isSigner": True
        },
        {
          "name": "programAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "dexProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "systemProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "rent",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "market",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": [
        {
          "name": "id",
          "type": "u8"
        }
      ]
    },
    {
      "name": "claim",
      "accounts": [
        {
          "name": "wallet",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "programAuthority",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "systemProgram",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": [
        {
          "name": "id",
          "type": "u8"
        }
      ],
      "returns": "u64"
    },
    {
      "name": "claimToken",
      "accounts": [
        {
          "name": "payer",
          "isMut": True,
          "isSigner": True
        },
        {
          "name": "wallet",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "programAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "programTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "destinationTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "mint",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "associatedTokenTokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "associatedTokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "systemProgram",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": [
        {
          "name": "id",
          "type": "u8"
        }
      ],
      "returns": "u64"
    },
    {
      "name": "createTokenLedger",
      "accounts": [
        {
          "name": "tokenLedger",
          "isMut": True,
          "isSigner": True
        },
        {
          "name": "payer",
          "isMut": True,
          "isSigner": True
        },
        {
          "name": "systemProgram",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "mercurialSwap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "swapState",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "poolAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "userTransferAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "sourceTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "destinationTokenAccount",
          "isMut": True,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "cykuraSwap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "signer",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "factoryState",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "poolState",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "inputTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "outputTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "inputVault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "outputVault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "lastObservationState",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "coreProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "serumSwap",
      "accounts": [
        {
          "name": "market",
          "accounts": [
            {
              "name": "market",
              "isMut": True,
              "isSigner": False
            },
            {
              "name": "openOrders",
              "isMut": True,
              "isSigner": False
            },
            {
              "name": "requestQueue",
              "isMut": True,
              "isSigner": False
            },
            {
              "name": "eventQueue",
              "isMut": True,
              "isSigner": False
            },
            {
              "name": "bids",
              "isMut": True,
              "isSigner": False
            },
            {
              "name": "asks",
              "isMut": True,
              "isSigner": False
            },
            {
              "name": "coinVault",
              "isMut": True,
              "isSigner": False
            },
            {
              "name": "pcVault",
              "isMut": True,
              "isSigner": False
            },
            {
              "name": "vaultSigner",
              "isMut": False,
              "isSigner": False
            }
          ]
        },
        {
          "name": "authority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "orderPayerTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "coinWallet",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "pcWallet",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "dexProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "rent",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "saberSwap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "swap",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "swapAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "userAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "inputUserAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "inputTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "outputUserAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "outputTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "feesTokenAccount",
          "isMut": True,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "saberAddDecimals",
      "accounts": [
        {
          "name": "addDecimalsProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "wrapper",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "wrapperMint",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "wrapperUnderlyingTokens",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "owner",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "userUnderlyingTokens",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userWrappedTokens",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "tokenSwap",
      "accounts": [
        {
          "name": "tokenSwapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "swap",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "authority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "userTransferAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "source",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "swapSource",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "swapDestination",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "destination",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "poolMint",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "poolFee",
          "isMut": True,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "tokenSwapV2",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "swap",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "authority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "userTransferAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "source",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "swapSource",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "swapDestination",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "destination",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "poolMint",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "poolFee",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "sourceMint",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "destinationMint",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "sourceTokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "destinationTokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "poolTokenProgram",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "senchaSwap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "swap",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "inputUserAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "inputTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "inputFeesAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "outputUserAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "outputTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "outputFeesAccount",
          "isMut": True,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "stepSwap",
      "accounts": [
        {
          "name": "tokenSwapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "swap",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "authority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "userTransferAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "source",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "swapSource",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "swapDestination",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "destination",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "poolMint",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "poolFee",
          "isMut": True,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "cropperSwap",
      "accounts": [
        {
          "name": "tokenSwapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "swap",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "swapState",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "authority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "userTransferAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "source",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "swapSource",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "swapDestination",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "destination",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "poolMint",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "poolFee",
          "isMut": True,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "raydiumSwap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "ammId",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "ammAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "ammOpenOrders",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "poolCoinTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "poolPcTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "serumProgramId",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "serumMarket",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "serumBids",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "serumAsks",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "serumEventQueue",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "serumCoinVaultAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "serumPcVaultAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "serumVaultSigner",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "userSourceTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userDestinationTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userSourceOwner",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "cremaSwap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "clmmConfig",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "clmmpool",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenA",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenB",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "accountA",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "accountB",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenAVault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenBVault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tickArrayMap",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "owner",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "partner",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "partnerAtaA",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "partnerAtaB",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "lifinitySwap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "authority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "amm",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "userTransferAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "sourceInfo",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "destinationInfo",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "swapSource",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "swapDestination",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "poolMint",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "feeAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "pythAccount",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "pythPcAccount",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "configAccount",
          "isMut": True,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "marinadeDeposit",
      "accounts": [
        {
          "name": "marinadeFinanceProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "state",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "msolMint",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "liqPoolSolLegPda",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "liqPoolMsolLeg",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "liqPoolMsolLegAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "reservePda",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "transferFrom",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "mintTo",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "msolMintAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "systemProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "userWsolTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tempWsolTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userTransferAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "payer",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "wsolMint",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "rent",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "marinadeUnstake",
      "accounts": [
        {
          "name": "marinadeFinanceProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "state",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "msolMint",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "liqPoolSolLegPda",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "liqPoolMsolLeg",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "treasuryMsolAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "getMsolFrom",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "getMsolFromAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "transferSolTo",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "systemProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "userWsolTokenAccount",
          "isMut": True,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "aldrinSwap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "pool",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "poolSigner",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "poolMint",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "baseTokenVault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "quoteTokenVault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "feePoolTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "walletAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "userBaseTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userQuoteTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "aldrinV2Swap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "pool",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "poolSigner",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "poolMint",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "baseTokenVault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "quoteTokenVault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "feePoolTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "walletAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "userBaseTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userQuoteTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "curve",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "whirlpoolSwap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "whirlpool",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenOwnerAccountA",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenVaultA",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenOwnerAccountB",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenVaultB",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tickArray0",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tickArray1",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tickArray2",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "oracle",
          "isMut": False,
          "isSigner": False,
          "docs": [
            "Oracle is currently unused and will be enabled on subsequent updates"
          ]
        }
      ],
      "args": []
    },
    {
      "name": "whirlpoolSwapV2",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgramA",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgramB",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "memoProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "whirlpool",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenMintA",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenMintB",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenOwnerAccountA",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenVaultA",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenOwnerAccountB",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenVaultB",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tickArray0",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tickArray1",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tickArray2",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "oracle",
          "isMut": True,
          "isSigner": False,
          "docs": [
            "Oracle is currently unused and will be enabled on subsequent updates"
          ]
        }
      ],
      "args": []
    },
    {
      "name": "invariantSwap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "state",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "pool",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tickmap",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "accountX",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "accountY",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "reserveX",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "reserveY",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "owner",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "programAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "meteoraSwap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "pool",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userSourceToken",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userDestinationToken",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "aVault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "bVault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "aTokenVault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "bTokenVault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "aVaultLpMint",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "bVaultLpMint",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "aVaultLp",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "bVaultLp",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "adminTokenFee",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "user",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "vaultProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "goosefxSwap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "controller",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "pair",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "sslIn",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "sslOut",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "liabilityVaultIn",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "swappedLiabilityVaultIn",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "liabilityVaultOut",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "swappedLiabilityVaultOut",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userInAta",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userOutAta",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "feeCollectorAta",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userWallet",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "feeCollector",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "deltafiSwap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "marketConfig",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "swapInfo",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userSourceToken",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userDestinationToken",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "swapSourceToken",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "swapDestinationToken",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "deltafiUser",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "adminDestinationToken",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "pythPriceBase",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "pythPriceQuote",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "userAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "balansolSwap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "authority",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "pool",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "taxMan",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "bidMint",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "treasurer",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "srcTreasury",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "srcAssociatedTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "askMint",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "dstTreasury",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "dstAssociatedTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "dstTokenAccountTaxman",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "systemProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "associatedTokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "rent",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "marcoPoloSwap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "state",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "pool",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenX",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenY",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "poolXAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "poolYAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "swapperXAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "swapperYAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "swapper",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "referrerXAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "referrerYAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "referrer",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "programAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "systemProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "associatedTokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "rent",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "dradexSwap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "pair",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "market",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "eventQueue",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "dexUser",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "marketUser",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "bids",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "asks",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "t0Vault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "t1Vault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "t0User",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "t1User",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "master",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "signer",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "systemProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "logger",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "lifinityV2Swap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "authority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "amm",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userTransferAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "sourceInfo",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "destinationInfo",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "swapSource",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "swapDestination",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "poolMint",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "feeAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "oracleMainAccount",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "oracleSubAccount",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "oraclePcAccount",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "raydiumClmmSwap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "payer",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "ammConfig",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "poolState",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "inputTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "outputTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "inputVault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "outputVault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "observationState",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tickArray",
          "isMut": True,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "raydiumClmmSwapV2",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "payer",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "ammConfig",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "poolState",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "inputTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "outputTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "inputVault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "outputVault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "observationState",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram2022",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "memoProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "inputVaultMint",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "outputVaultMint",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "phoenixSwap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "logAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "market",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "trader",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "baseAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "quoteAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "baseVault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "quoteVault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "symmetrySwap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "buyer",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "fundState",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "pdaAccount",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "pdaFromTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "buyerFromTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "pdaToTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "buyerToTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "swapFeeAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "hostFeeAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "managerFeeAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenList",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "prismData",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "heliumTreasuryManagementRedeemV0",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "treasuryManagement",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "treasuryMint",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "supplyMint",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "treasury",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "circuitBreaker",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "from",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "to",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "owner",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "circuitBreakerProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "goosefxV2Swap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "pair",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "poolRegistry",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userWallet",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "sslPoolInSigner",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "sslPoolOutSigner",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "userAtaIn",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userAtaOut",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "sslOutMainVault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "sslOutSecondaryVault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "sslInMainVault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "sslInSecondaryVault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "sslOutFeeVault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "feeDestination",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "outputTokenPriceHistory",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "outputTokenOracle",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "inputTokenPriceHistory",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "inputTokenOracle",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "eventEmitter",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "perpsSwap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "owner",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "fundingAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "receivingAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "transferAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "perpetuals",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "pool",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "receivingCustody",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "receivingCustodyOracleAccount",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "receivingCustodyTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "dispensingCustody",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "dispensingCustodyOracleAccount",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "dispensingCustodyTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "eventAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "program",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "perpsAddLiquidity",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "owner",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "fundingOrReceivingAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "lpTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "transferAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "perpetuals",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "pool",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "custody",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "custodyOracleAccount",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "custodyTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "lpTokenMint",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "eventAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "program",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "perpsRemoveLiquidity",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "owner",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "fundingOrReceivingAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "lpTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "transferAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "perpetuals",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "pool",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "custody",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "custodyOracleAccount",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "custodyTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "lpTokenMint",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "eventAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "program",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "meteoraDlmmSwap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "lbPair",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "binArrayBitmapExtension",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "reserveX",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "reserveY",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userTokenIn",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userTokenOut",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenXMint",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenYMint",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "oracle",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "hostFeeIn",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "user",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenXProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenYProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "eventAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "program",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "openBookV2Swap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "signer",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "penaltyPayer",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "market",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "marketAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "bids",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "asks",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "marketBaseVault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "marketQuoteVault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "eventHeap",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userBaseAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userQuoteAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "oracleA",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "oracleB",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "systemProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "openOrdersAdmin",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "cloneSwap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "user",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "clone",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "pools",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "oracles",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userCollateralTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userOnassetTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "onassetMint",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "collateralMint",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "collateralVault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "treasuryOnassetTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "treasuryCollateralTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "cloneStaking",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "userStakingAccount",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "cloneStakingProgram",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "raydiumCpSwap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "payer",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "authority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "ammConfig",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "poolState",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "inputTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "outputTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "inputVault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "outputVault",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "inputTokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "outputTokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "inputTokenMint",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "outputTokenMint",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "observationState",
          "isMut": True,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "oneIntroSwap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "metadataState",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "poolState",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "poolAuthPda",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "poolTokenInAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "poolTokenOutAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "user",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userTokenInAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userTokenOutAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "metadataSwapFeeAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "referralTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "pumpdotfunWrappedBuy",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "global",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "feeRecipient",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "mint",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "bondingCurve",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "associatedBondingCurve",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "associatedUser",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "user",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "systemProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "rent",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "eventAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "program",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "userWsolTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tempWsolTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "wsolMint",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "pumpdotfunWrappedSell",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "global",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "feeRecipient",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "mint",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "bondingCurve",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "associatedBondingCurve",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "associatedUser",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "user",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "systemProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "associatedTokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "eventAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "program",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "userWsolTokenAccount",
          "isMut": True,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "perpsV2Swap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "owner",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "fundingAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "receivingAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "transferAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "perpetuals",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "pool",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "receivingCustody",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "receivingCustodyDovesPriceAccount",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "receivingCustodyPythnetPriceAccount",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "receivingCustodyTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "dispensingCustody",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "dispensingCustodyDovesPriceAccount",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "dispensingCustodyPythnetPriceAccount",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "dispensingCustodyTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "eventAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "program",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "perpsV2AddLiquidity",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "owner",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "fundingOrReceivingAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "lpTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "transferAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "perpetuals",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "pool",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "custody",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "custodyDovesPriceAccount",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "custodyPythnetPriceAccount",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "custodyTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "lpTokenMint",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "eventAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "program",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "perpsV2RemoveLiquidity",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "owner",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "fundingOrReceivingAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "lpTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "transferAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "perpetuals",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "pool",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "custody",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "custodyDovesPriceAccount",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "custodyPythnetPriceAccount",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "custodyTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "lpTokenMint",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "eventAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "program",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "moonshotWrappedBuy",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "sender",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "senderTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "curveAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "curveTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "dexFee",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "helioFee",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "mint",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "configAccount",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "associatedTokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "systemProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "userWsolTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "tempWsolTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "wsolMint",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "moonshotWrappedSell",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "sender",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "senderTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "curveAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "curveTokenAccount",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "dexFee",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "helioFee",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "mint",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "configAccount",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "associatedTokenProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "systemProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "userWsolTokenAccount",
          "isMut": True,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "stabbleStableSwap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "user",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "userTokenIn",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userTokenOut",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "vaultTokenIn",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "vaultTokenOut",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "beneficiaryTokenOut",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "pool",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "withdrawAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "vault",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "vaultAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "vaultProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "stabbleWeightedSwap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "user",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "userTokenIn",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userTokenOut",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "vaultTokenIn",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "vaultTokenOut",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "beneficiaryTokenOut",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "pool",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "withdrawAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "vault",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "vaultAuthority",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "vaultProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    },
    {
      "name": "obricSwap",
      "accounts": [
        {
          "name": "swapProgram",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tradingPair",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "mintX",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "mintY",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "reserveX",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "reserveY",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userTokenAccountX",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "userTokenAccountY",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "protocolFee",
          "isMut": True,
          "isSigner": False
        },
        {
          "name": "xPriceFeed",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "yPriceFeed",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "user",
          "isMut": False,
          "isSigner": False
        },
        {
          "name": "tokenProgram",
          "isMut": False,
          "isSigner": False
        }
      ],
      "args": []
    }
  ],
  "accounts": [
    {
      "name": "TokenLedger",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "tokenAccount",
            "type": "publicKey"
          },
          {
            "name": "amount",
            "type": "u64"
          }
        ]
      }
    }
  ],
  "types": [
    {
      "name": "AmountWithSlippage",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "amount",
            "type": "u64"
          },
          {
            "name": "slippageBps",
            "type": "u16"
          }
        ]
      }
    },
    {
      "name": "RoutePlanStep",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "swap",
            "type": {
              "defined": "Swap"
            }
          },
          {
            "name": "percent",
            "type": "u8"
          },
          {
            "name": "inputIndex",
            "type": "u8"
          },
          {
            "name": "outputIndex",
            "type": "u8"
          }
        ]
      }
    },
    {
      "name": "Side",
      "type": {
        "kind": "enum",
        "variants": [
          {
            "name": "Bid"
          },
          {
            "name": "Ask"
          }
        ]
      }
    },
    {
      "name": "Swap",
      "type": {
        "kind": "enum",
        "variants": [
          {
            "name": "Saber"
          },
          {
            "name": "SaberAddDecimalsDeposit"
          },
          {
            "name": "SaberAddDecimalsWithdraw"
          },
          {
            "name": "TokenSwap"
          },
          {
            "name": "Sencha"
          },
          {
            "name": "Step"
          },
          {
            "name": "Cropper"
          },
          {
            "name": "Raydium"
          },
          {
            "name": "Crema",
            "fields": [
              {
                "name": "aToB",
                "type": "bool"
              }
            ]
          },
          {
            "name": "Lifinity"
          },
          {
            "name": "Mercurial"
          },
          {
            "name": "Cykura"
          },
          {
            "name": "Serum",
            "fields": [
              {
                "name": "side",
                "type": {
                  "defined": "Side"
                }
              }
            ]
          },
          {
            "name": "MarinadeDeposit"
          },
          {
            "name": "MarinadeUnstake"
          },
          {
            "name": "Aldrin",
            "fields": [
              {
                "name": "side",
                "type": {
                  "defined": "Side"
                }
              }
            ]
          },
          {
            "name": "AldrinV2",
            "fields": [
              {
                "name": "side",
                "type": {
                  "defined": "Side"
                }
              }
            ]
          },
          {
            "name": "Whirlpool",
            "fields": [
              {
                "name": "aToB",
                "type": "bool"
              }
            ]
          },
          {
            "name": "Invariant",
            "fields": [
              {
                "name": "xToY",
                "type": "bool"
              }
            ]
          },
          {
            "name": "Meteora"
          },
          {
            "name": "GooseFX"
          },
          {
            "name": "DeltaFi",
            "fields": [
              {
                "name": "stable",
                "type": "bool"
              }
            ]
          },
          {
            "name": "Balansol"
          },
          {
            "name": "MarcoPolo",
            "fields": [
              {
                "name": "xToY",
                "type": "bool"
              }
            ]
          },
          {
            "name": "Dradex",
            "fields": [
              {
                "name": "side",
                "type": {
                  "defined": "Side"
                }
              }
            ]
          },
          {
            "name": "LifinityV2"
          },
          {
            "name": "RaydiumClmm"
          },
          {
            "name": "Openbook",
            "fields": [
              {
                "name": "side",
                "type": {
                  "defined": "Side"
                }
              }
            ]
          },
          {
            "name": "Phoenix",
            "fields": [
              {
                "name": "side",
                "type": {
                  "defined": "Side"
                }
              }
            ]
          },
          {
            "name": "Symmetry",
            "fields": [
              {
                "name": "fromTokenId",
                "type": "u64"
              },
              {
                "name": "toTokenId",
                "type": "u64"
              }
            ]
          },
          {
            "name": "TokenSwapV2"
          },
          {
            "name": "HeliumTreasuryManagementRedeemV0"
          },
          {
            "name": "StakeDexStakeWrappedSol"
          },
          {
            "name": "StakeDexSwapViaStake",
            "fields": [
              {
                "name": "bridgeStakeSeed",
                "type": "u32"
              }
            ]
          },
          {
            "name": "GooseFXV2"
          },
          {
            "name": "Perps"
          },
          {
            "name": "PerpsAddLiquidity"
          },
          {
            "name": "PerpsRemoveLiquidity"
          },
          {
            "name": "MeteoraDlmm"
          },
          {
            "name": "OpenBookV2",
            "fields": [
              {
                "name": "side",
                "type": {
                  "defined": "Side"
                }
              }
            ]
          },
          {
            "name": "RaydiumClmmV2"
          },
          {
            "name": "StakeDexPrefundWithdrawStakeAndDepositStake",
            "fields": [
              {
                "name": "bridgeStakeSeed",
                "type": "u32"
              }
            ]
          },
          {
            "name": "Clone",
            "fields": [
              {
                "name": "poolIndex",
                "type": "u8"
              },
              {
                "name": "quantityIsInput",
                "type": "bool"
              },
              {
                "name": "quantityIsCollateral",
                "type": "bool"
              }
            ]
          },
          {
            "name": "SanctumS",
            "fields": [
              {
                "name": "srcLstValueCalcAccs",
                "type": "u8"
              },
              {
                "name": "dstLstValueCalcAccs",
                "type": "u8"
              },
              {
                "name": "srcLstIndex",
                "type": "u32"
              },
              {
                "name": "dstLstIndex",
                "type": "u32"
              }
            ]
          },
          {
            "name": "SanctumSAddLiquidity",
            "fields": [
              {
                "name": "lstValueCalcAccs",
                "type": "u8"
              },
              {
                "name": "lstIndex",
                "type": "u32"
              }
            ]
          },
          {
            "name": "SanctumSRemoveLiquidity",
            "fields": [
              {
                "name": "lstValueCalcAccs",
                "type": "u8"
              },
              {
                "name": "lstIndex",
                "type": "u32"
              }
            ]
          },
          {
            "name": "RaydiumCP"
          },
          {
            "name": "WhirlpoolSwapV2",
            "fields": [
              {
                "name": "aToB",
                "type": "bool"
              },
              {
                "name": "remainingAccountsInfo",
                "type": {
                  "option": {
                    "defined": "RemainingAccountsInfo"
                  }
                }
              }
            ]
          },
          {
            "name": "OneIntro"
          },
          {
            "name": "PumpdotfunWrappedBuy"
          },
          {
            "name": "PumpdotfunWrappedSell"
          },
          {
            "name": "PerpsV2"
          },
          {
            "name": "PerpsV2AddLiquidity"
          },
          {
            "name": "PerpsV2RemoveLiquidity"
          },
          {
            "name": "MoonshotWrappedBuy"
          },
          {
            "name": "MoonshotWrappedSell"
          },
          {
            "name": "StabbleStableSwap"
          },
          {
            "name": "StabbleWeightedSwap"
          },
          {
            "name": "Obric",
            "fields": [
              {
                "name": "x_to_y",
                "type": "bool"
              }
            ]
          }
        ]
      }
    },
    {
      "name": "RemainingAccountsSlice",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "accountsType",
            "type": {
              "defined": "AccountsType"
            }
          },
          {
            "name": "length",
            "type": "u8"
          }
        ]
      }
    },
    {
      "name": "RemainingAccountsInfo",
      "type": {
        "kind": "struct",
        "fields": [
          {
            "name": "slices",
            "type": {
              "vec": {
                "defined": "RemainingAccountsSlice"
              }
            }
          }
        ]
      }
    },
    {
      "name": "AccountsType",
      "type": {
        "kind": "enum",
        "variants": [
          {
            "name": "TransferHookA"
          },
          {
            "name": "TransferHookB"
          }
        ]
      }
    }
  ],
  "events": [
    {
      "name": "SwapEvent",
      "fields": [
        {
          "name": "amm",
          "type": "publicKey",
          "index": False
        },
        {
          "name": "inputMint",
          "type": "publicKey",
          "index": False
        },
        {
          "name": "inputAmount",
          "type": "u64",
          "index": False
        },
        {
          "name": "outputMint",
          "type": "publicKey",
          "index": False
        },
        {
          "name": "outputAmount",
          "type": "u64",
          "index": False
        }
      ]
    },
    {
      "name": "FeeEvent",
      "fields": [
        {
          "name": "account",
          "type": "publicKey",
          "index": False
        },
        {
          "name": "mint",
          "type": "publicKey",
          "index": False
        },
        {
          "name": "amount",
          "type": "u64",
          "index": False
        }
      ]
    }
  ],
  "errors": [
    {
      "code": 6000,
      "name": "EmptyRoute",
      "msg": "Empty route"
    },
    {
      "code": 6001,
      "name": "SlippageToleranceExceeded",
      "msg": "Slippage tolerance exceeded"
    },
    {
      "code": 6002,
      "name": "InvalidCalculation",
      "msg": "Invalid calculation"
    },
    {
      "code": 6003,
      "name": "MissingPlatformFeeAccount",
      "msg": "Missing platform fee account"
    },
    {
      "code": 6004,
      "name": "InvalidSlippage",
      "msg": "Invalid slippage"
    },
    {
      "code": 6005,
      "name": "NotEnoughPercent",
      "msg": "Not enough percent to 100"
    },
    {
      "code": 6006,
      "name": "InvalidInputIndex",
      "msg": "Token input index is invalid"
    },
    {
      "code": 6007,
      "name": "InvalidOutputIndex",
      "msg": "Token output index is invalid"
    },
    {
      "code": 6008,
      "name": "NotEnoughAccountKeys",
      "msg": "Not Enough Account keys"
    },
    {
      "code": 6009,
      "name": "NonZeroMinimumOutAmountNotSupported",
      "msg": "Non zero minimum out amount not supported"
    },
    {
      "code": 6010,
      "name": "InvalidRoutePlan",
      "msg": "Invalid route plan"
    },
    {
      "code": 6011,
      "name": "InvalidReferralAuthority",
      "msg": "Invalid referral authority"
    },
    {
      "code": 6012,
      "name": "LedgerTokenAccountDoesNotMatch",
      "msg": "Token account doesn't match the ledger"
    },
    {
      "code": 6013,
      "name": "InvalidTokenLedger",
      "msg": "Invalid token ledger"
    },
    {
      "code": 6014,
      "name": "IncorrectTokenProgramID",
      "msg": "Token program ID is invalid"
    },
    {
      "code": 6015,
      "name": "TokenProgramNotProvided",
      "msg": "Token program not provided"
    },
    {
      "code": 6016,
      "name": "SwapNotSupported",
      "msg": "Swap not supported"
    },
    {
      "code": 6017,
      "name": "ExactOutAmountNotMatched",
      "msg": "Exact out amount doesn't match"
    }
  ]
}
