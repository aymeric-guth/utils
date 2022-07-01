#include <stdio.h>


int64_t lin_intp(int64_t v, int64_t xa, int64_t ya, int64_t xb, int64_t yb)
{
    return (v - xa) * (yb - xb) / (ya - xa) + xb;
}

int main(int argc, char **argv)
{
    int64_t res = lin_intp(10, 0, 100, 100, 1000);
    printf("%lld\n", res);
    return 0;
}
