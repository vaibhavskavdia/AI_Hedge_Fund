import { useState } from "react";
import axios from "axios";

import {
  getSectorIntelligence,
} from "../../../services/sector";

export function useSector() {
  const [loading, setLoading] =
    useState(false);

  const [sector, setSector] =
    useState<any>(null);

  const [error, setError] =
    useState<string | null>(null);

  const searchSector = async (
    value: string
  ) => {
    try {
      setLoading(true);

      setError(null);

      const response =
        await getSectorIntelligence(
          value
        );

      setSector(response);
    } catch (err) {
      console.error(err);

      if (axios.isAxiosError(err)) {
        if (
          typeof err.response?.data?.detail ===
          "string"
        ) {
          setError(
            err.response.data.detail
          );
        } else {
          setError("Unable to fetch sector.");
        }
      } else if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Unexpected error.");
      }
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,

    sector,

    error,

    searchSector,
  };
}