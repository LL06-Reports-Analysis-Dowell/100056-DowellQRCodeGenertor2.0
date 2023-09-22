import Link from 'next/link';
const Header = () => {
  return (
    <header className="bg-blue-500 py-4">
      <div className="container mx-auto flex justify-between items-center">
        <h1 className="text-2xl font-bold text-white">QR Code App</h1>
        <nav className="space-x-4 text-white">
          <Link href="/">Home</Link>
          <Link href="../GetRoute">QR Codes</Link>
          <Link href="/PutRoute">Update Link And Words</Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;
