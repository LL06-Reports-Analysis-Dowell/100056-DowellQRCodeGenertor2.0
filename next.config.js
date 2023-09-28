/** @type {import('next').NextConfig} */
const nextConfig = {
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
