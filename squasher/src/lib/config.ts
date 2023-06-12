import { mkdir, readFile, writeFile } from "fs/promises";

export type Config = {
  credential: string;
};

const configDir = `${process.env["APPDATA"]}/lapsquash/squasher`;
const configPath = `${process.env["APPDATA"]}/lapsquash/squasher/config.json`;

export const saveConfig = async (config: Config): Promise<void> => {
  await mkdir(configDir, { recursive: true });
  await writeFile(configPath, JSON.stringify(config));
};

export const readConfig = async (): Promise<Config> => {
  const config = await readFile(configPath, "utf-8");
  return JSON.parse(config);
};
