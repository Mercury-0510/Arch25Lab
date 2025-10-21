/*
 * This is a legacy rpc/netdb.h header for compatibility.
 * Source: glibc 2.28 (public domain, for educational/lab use only)
 */
#ifndef _RPC_NETDB_H
#define _RPC_NETDB_H 1

#include <features.h>
#include <netdb.h>
#include <rpc/types.h>

__BEGIN_DECLS

struct rpcent
{
  char *r_name;    /* name of server for this rpc program */
  char **r_aliases;    /* alias list */
  long r_number;   /* rpc program number */
};

extern void setrpcent (int __stayopen);
extern void endrpcent (void);
extern struct rpcent *getrpcbyname (const char *__name);
extern struct rpcent *getrpcbynumber (int __number);
extern struct rpcent *getrpcent (void);
extern int getrpcbyname_r (const char *__name, struct rpcent *__result_buf,
                          char *__buffer, size_t __buflen,
                          struct rpcent **__result);
extern int getrpcbynumber_r (int __number, struct rpcent *__result_buf,
                            char *__buffer, size_t __buflen,
                            struct rpcent **__result);
extern int getrpcent_r (struct rpcent *__result_buf, char *__buffer,
                       size_t __buflen, struct rpcent **__result);

__END_DECLS

#endif /* rpc/netdb.h */
