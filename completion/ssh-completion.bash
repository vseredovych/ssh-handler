#!/usr/bin/env bash

#list of users
users=('vsere' 'vsere' 'user' 'smykytiu' 'smykytiu' 'smykytiu')
#users=('aaa' 'bbb' 'smykytiu')
#list of hosts
hosts=('localhost' 'host1' 'host2' 'localhost1' 'localhost2' 'localhost3')
#hosts=('host1' 'host2')
users_hosts=()

for u in "${users[@]}"
  do
  for h in "${hosts[@]}"
    do
      users_hosts=("${users_hosts[@]}" "${u}@${h}")
    done
done

_ssh_completions()
{
  # if there is more then one args, stop suggestions
  if [ "${#COMP_WORDS[@]}" != "2" ]; then
    return
  fi

  # if arg contain '@' suggest host
  if [[ "${COMP_WORDS[1]}" =~ "@" ]]; then
    # separete arg by '@' and add '@' to the end
    # idea: remove everyting after '@' to have pure username
    user="${COMP_WORDS[1]%%@*}@"

    # add username as prefix tp the list of hostnames
    user_hosts=( "${hosts[@]/#/${user}}" )

    # suggest 'user' + '@' + 'hostnames'
    COMPREPLY=($(compgen -W "${user_hosts[*]}" "${COMP_WORDS[1]}"))

  # else suggest user
  else

    #user="${COMP_WORDS[1]%%@*}@"
    # suggest 'user'
    #user_hosts=( "${hosts[@]/#/${user}}" )
    COMPREPLY=($(compgen -W "${users_hosts[*]}" "${COMP_WORDS[1]}"))
    #COMPREPLY="${COMPREPLY}"
 fi
}

complete -F _ssh_completions ssh

