// client/src/pages/Splash.jsx
import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Lottie from "lottie-react";
import airplaneAnim from "../assets/airplane-loading.json";

/**
 * Splash (Tailwind version)
 * - shows Lottie airplane animation
 * - shows "Cargando..." with 3 animated dots
 * - waits 3 seconds then navigates to /home
 */

export default function Splash() {
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate("/home", { replace: true });
    }, 2000);

    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-blue-50 to-blue-100">
      <div className="flex flex-col items-center gap-6 p-6 rounded-xl bg-blue-50 backdrop-blur-sm shadow-xl">
        <div className="w-44 h-44 md:w-52 md:h-52">
          <Lottie animationData={airplaneAnim} loop={true} />
        </div>

        <div className="flex items-center gap-2 text-blue-800 font-semibold">
          <span className="text-lg md:text-xl">Cargando</span>
          <span className="flex items-center gap-1">
            <span
              className="inline-block w-2 h-2 rounded-full bg-blue-700 animate-bounce"
              style={{ animationDelay: "0s" }}
            />
            <span
              className="inline-block w-2 h-2 rounded-full bg-blue-700 animate-bounce"
              style={{ animationDelay: "0.15s" }}
            />
            <span
              className="inline-block w-2 h-2 rounded-full bg-blue-700 animate-bounce"
              style={{ animationDelay: "0.3s" }}
            />
          </span>
        </div>
      </div>
    </div>
  );
}
