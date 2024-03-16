import { useState } from "react";

// eslint-disable-next-line react/prop-types
export default function Input({ type, name, label, state, set }) {
  const [labelTop, setLabelTop] = useState(false);
  return (
    <div className="w-full mx-auto h-10 relative">
      <label
        htmlFor={name}
        className={`absolute transition-all duration-200 ${
          labelTop ? "-top-3 text-primary bg-white" : "-translate-y-1/2 top-1/2"
        } left-2`}
      >
        {label}
      </label>
      <input
        type={type}
        name={name}
        id={name}
        value={state}
        className="w-full h-full border-[1px] border-black focus:outline-primary px-2"
        onFocus={() => setLabelTop(true)}
        onBlur={() => !state && setLabelTop(false)}
        onChange={(e) => set(e.target.value)}
      />
    </div>
  );
}
