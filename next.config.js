/** @type {import('next').NextConfig} */
const nextConfig = {
    output: 'export',
    images: {
        remotePatterns: [
          {
            protocol: 'http',
            hostname: 'dowellfileuploader.uxlivinglab.online',
            port: '',
            pathname: '/qrCodes/**',
          },
        ],
      },
}

module.exports = nextConfig
