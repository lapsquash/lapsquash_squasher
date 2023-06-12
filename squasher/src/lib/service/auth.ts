import { exec } from "child_process";
import { IncomingMessage, createServer } from "http";
import { ENV } from "../../lib/env";

const request2authCode = (req: IncomingMessage) => {
  const url = new URL(req.url!, "http://localhost:3000");
  const searchParams = url.searchParams;
  return searchParams.get("code") ?? undefined;
};

export async function serveAuthCode(timeoutMs: number): Promise<string> {
  const server = createServer();

  return new Promise<string>((resolve, reject) => {
    server.listen(3000, () => {
      console.log("🔥 Server listening on port 3000...\n");
    });

    server.on("request", async (req, res) => {
      const authCode = request2authCode(req);

      if (authCode == undefined) {
        res.end("No auth code found");
        reject(new Error("No auth code found"));
        return;
      }

      res.end("You can close this window now");

      resolve(authCode!);
      return;
    });

    setTimeout(() => {
      server.close();
      reject(new Error("Authentication Timeout"));
    }, timeoutMs);
  });
}

export const runAuthRedirect = async (): Promise<void> => {
  const queries = {
    client_id: ENV.CLIENT_ID,
    response_type: "code",
    redirect_uri: ENV.REDIRECT_URI,
    response_mode: "query",
    scope: "Sites.ReadWrite.All",
  };
  const query = new URLSearchParams(queries).toString();
  const url = [
    "https://login.microsoftonline.com/",
    ENV.TENANT_ID,
    "/oauth2/v2.0/authorize?",
    query,
  ];

  console.log(`🌐 Opening browser...\n  ${url.join("")}\n`);

  if (process.platform === "win32") {
    exec(`start ${url.join("").replaceAll("&", "^&")}`);
  } else {
    exec(`open ${url.join("")}`);
  }
};
