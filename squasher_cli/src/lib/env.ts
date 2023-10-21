import * as dotenv from "dotenv";
import path from "path";

dotenv.config({ path: path.resolve(__dirname, "../../.env") });

export const ENV = {
  TENANT_ID: process.env["TENANT_ID"] as string,
  CLIENT_ID: process.env["CLIENT_ID"] as string,
  REDIRECT_URI: process.env["REDIRECT_URI"] as string,
  RELAY_SERVER_URL: process.env["RELAY_SERVER_URL"] as string,
} as const;

const missingEnv = Object.entries(ENV).filter(([, value]) => !value);
if (missingEnv.length) {
  throw new Error(
    `Missing environment variables: ${missingEnv
      .map(([key]) => key)
      .join(", ")}`
  );
}
