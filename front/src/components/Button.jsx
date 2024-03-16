// eslint-disable-next-line react/prop-types
export default function Button({ text, loading, textLoading }) {
  return (
    <button
      className={`w-full bg-primary text-white font-semibold text-lg py-1`}
    >
      {loading ? textLoading : text}
    </button>
  );
}
