import { exec } from "child_process";
import { createServer } from "http";
import { ENV } from "../../lib/env";

export const getCode = async (): Promise<string> =>
  new Promise((resolve, reject) => {
    const server = createServer((req, res) => {
      const code = req.url?.split("code=")[1];
      if (code) {
        res.end("You can close this window now.");
        return resolve(code);
      } else {
        res.end("No code found.");
        return reject("No code found.");
      }
    });

    server.listen(new URL(ENV.REDIRECT_URI).port, () => {
      console.log("Server listening...");
    });
  });

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

  console.log("Opening browser..." + url.join(""));

  if (process.platform === "win32") {
    exec(`start ${url.join("").replaceAll("&", "^&")}`);
  } else {
    exec(`open ${url.join("")}`);
  }
};
