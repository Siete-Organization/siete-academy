import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { AxiosError, type AxiosResponse, type InternalAxiosRequestConfig } from "axios";
import { api } from "./api";

vi.mock("./firebase", () => ({ getIdToken: async () => null }));

function badGateway(config: InternalAxiosRequestConfig) {
  const response = {
    data: "Bad Gateway",
    status: 502,
    statusText: "Bad Gateway",
    headers: {},
    config,
  } as AxiosResponse;
  return new AxiosError("Bad Gateway", "ERR_BAD_RESPONSE", config, null, response);
}

describe("api retry interceptor", () => {
  const originalAdapter = api.defaults.adapter;

  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    api.defaults.adapter = originalAdapter;
    vi.useRealTimers();
  });

  it("reintenta GETs ante 502 y resuelve cuando el server vuelve", async () => {
    let calls = 0;
    api.defaults.adapter = async (config) => {
      calls++;
      if (calls < 3) throw badGateway(config);
      return {
        data: { ok: true },
        status: 200,
        statusText: "OK",
        headers: {},
        config,
      } as AxiosResponse;
    };

    const promise = api.get("/cohorts");
    await vi.runAllTimersAsync();
    const res = await promise;

    expect(res.status).toBe(200);
    expect(calls).toBe(3);
  });

  it("no reintenta POSTs (evita duplicar entregas/postulaciones)", async () => {
    let calls = 0;
    api.defaults.adapter = async (config) => {
      calls++;
      throw badGateway(config);
    };

    const promise = api.post("/applications", {}).catch((e: AxiosError) => e);
    await vi.runAllTimersAsync();
    const err = await promise;

    expect((err as AxiosError).response?.status).toBe(502);
    expect(calls).toBe(1);
  });

  it("no reintenta errores no transitorios (404)", async () => {
    let calls = 0;
    api.defaults.adapter = async (config) => {
      calls++;
      const response = {
        data: "",
        status: 404,
        statusText: "Not Found",
        headers: {},
        config,
      } as AxiosResponse;
      throw new AxiosError("Not Found", "ERR_BAD_REQUEST", config, null, response);
    };

    const promise = api.get("/nope").catch((e: AxiosError) => e);
    await vi.runAllTimersAsync();
    const err = await promise;

    expect((err as AxiosError).response?.status).toBe(404);
    expect(calls).toBe(1);
  });

  it("se rinde tras agotar los reintentos", async () => {
    let calls = 0;
    api.defaults.adapter = async (config) => {
      calls++;
      throw badGateway(config);
    };

    const promise = api.get("/cohorts").catch((e: AxiosError) => e);
    await vi.runAllTimersAsync();
    const err = await promise;

    expect((err as AxiosError).response?.status).toBe(502);
    expect(calls).toBe(7); // 1 intento + 6 reintentos
  });
});
