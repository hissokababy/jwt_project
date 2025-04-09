from os import chmod
from Crypto.PublicKey import RSA

key = RSA.generate(2048)
print(key.exportKey('PEM'))

pubkey = key.publickey().exportKey('OpenSSH')
print(pubkey)

PRIVATE_KEY = b'-----BEGIN RSA PRIVATE KEY-----\nMIIEogIBAAKCAQEAqikoCSSbqxzk+TdmnkcaV04Ufi3GVlPUylQyiR1+ApzMqNRr\nvJQy/MHRnBqURpvNyInOQOJkUmF7mT4IyssYh0N1K8BBSHjp3EDppaQ7DFZiVWoT\nePU8j55PHFKVDovt5AGc4Sq+R8rY8UgJ1RRjxj+jyPze6XTspMnk0TY+pfzNIP3N\npzWs16cvCslpFiVtgMUJJTENwyFhoEeMI+zD55QXgy4e5JBPkZ9rAfUBll6PjuQ7\nR+RquHG7U4vte/2e5hwn505Wo0XV+LVuZGf3JRkqcv7TRlic8LUkxGgcxDkJxkXL\nDtB7Z8qatsZW7C+R5n8t2SxL8Mm5YU99hLmcHQIDAQABAoIBAAw+Xd60JaDp7IfW\n6dyMEGPyMemwvX6xe+dhdSlsiwg0Sn2ZznUi0yOT7QZaDnIHyYZoDZ3/+QJi3uCn\nfnAPeqC9xKaOdNdHUmLb9A1/hBT4YKb1gcuVFo1Dvm/mEuRmQr3CZ/L25ZSHQfwX\nS0drtvb2CU28jdJahjrtOmuoIL95eepgh8KzKWd6IUfhPe1CZSl+HBx39darvAKQ\nUDml3O8zbO+GiWkM+3QEwjfRxb32FiENDSuYwdfLwlJwkpRRvBTmp/Upt6F4wmIt\n3zgLYWV6YL6cHFEti9g091qt0qqdxc2L5xFQwDnuSuhuc6EwisAaBIOlxAPxKxZC\nB9tEMrkCgYEAxK3HIEdsbcbtxNpUVP7tQuLxD7JKHLmig6cKcrUztWcAXEGKR1N8\nyN+PZ7OVrmWJ39zF0NICQ7JRh+gA2CCBATckpvPyiVqNJeoBbiqWl9tFM90IaiO1\n6XxP+XjK5Mjxl7XI3eYuPyfMV6P0IssF3iOr/hpXbEWNktEV3V6+NQ8CgYEA3XvU\n/reutGw8S1ptE3ooa/w4TFj99vPphEYXv/fZbI7YmsMn+K7ZIOJNWGt+Ly4EY71T\nK/NmpTPQemVqG6DI1gsQbfWtlN5iAjhWxFcJH6jowRdWpTdhhY/t7uy96e9mFajx\nw5hNjKVaZbacISuC/4ihS4mMjw5uQb0MtmEhlBMCgYBQrgi1URdFoQkAa5+Ujk69\n1WKV0cldJzlnUCqVC4f+rhYTwj77K2BQ9oRZQe3w8G4yitoK41tScd/IJH/UKOFC\nomBCrGeduKuWFfwoOQg1mxk0QUOmZqfE893KtKZmW5ffaA7SGA54kdbdTMBlVWs+\nyNtRDXU3UQDWbTbO7IKSOQKBgG39ax871NTg02iQdY6woZZO4R55K1YSdysrK+w3\nh5AzuDnTJOyI2GdOOx7n8vg3IBLwGHfBHn54JtZButoRlOtG/1e8JAHEFmQH2n8S\nwgMo/L23e139DL8pZP28L+wW6VlkVvvNjOWF0Eim0Q5f72Q7U+6RVm5MulCHM+L2\nhZhlAoGATUKhw4v9A7CQQgxN9QoM1iVYOT4A/fCaMEF3kiKJdZH+4DuGr45377Nx\nO31AOuisW4jxm6QLp1ohcZpO8cYLBpAU/V5v8/WTq/ai+MyoxQfgAue2Ytf0gPeZ\n8sg/qBC+6h9PpfSPxRSQaequilfve35PkZ1eWKziUpBCIDKHocg=\n-----END RSA PRIVATE KEY-----'

PUBLIC_KEY = b'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCqKSgJJJurHOT5N2aeRxpXThR+LcZWU9TKVDKJHX4CnMyo1Gu8lDL8wdGcGpRGm83Iic5A4mRSYXuZPgjKyxiHQ3UrwEFIeOncQOmlpDsMVmJVahN49TyPnk8cUpUOi+3kAZzhKr5HytjxSAnVFGPGP6PI/N7pdOykyeTRNj6l/M0g/c2nNazXpy8KyWkWJW2AxQklMQ3DIWGgR4wj7MPnlBeDLh7kkE+Rn2sB9QGWXo+O5DtH5Gq4cbtTi+17/Z7mHCfnTlajRdX4tW5kZ/clGSpy/tNGWJzwtSTEaBzEOQnGRcsO0Htnypq2xlbsL5Hmfy3ZLEvwyblhT32EuZwd'

# with open("/tmp/private.key", 'wb') as content_file:
#     chmod("/tmp/private.key", 0o600) #use an 0o prefix for octal integers
#     content_file.write(key.exportKey('PEM'))

# pubkey = key.publickey()
# with open("/tmp/public.key", 'wb') as content_file:
#     content_file.write(pubkey.exportKey('OpenSSH'))
