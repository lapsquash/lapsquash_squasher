import { createTRPCProxyClient, httpBatchLink } from "@trpc/client";

import type { AppRouter } from "@analyzer";

export const analyzer = {
  public: createTRPCProxyClient<AppRouter>({
    links: [
      httpBatchLink({
        url: "http://127.0.0.1:8787/trpc",
      }),
    ],
  }),
  protected: (credential: string) =>
    createTRPCProxyClient<AppRouter>({
      links: [
        httpBatchLink({
          url: "http://127.0.0.1:8787/trpc",
          headers: {
            authorization: `Bearer ${credential}`,
          },
        }),
      ],
    }),
};
