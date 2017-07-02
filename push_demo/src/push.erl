-module(push).
-compile(export_all).


make_json(Msg) ->
    PushMap = #{
      id => 228267026,
      message => Msg
     },
    jsx:encode(PushMap).


push(Host, Port, Msg) ->
    {ok, Socket} = gen_tcp:connect(Host, Port, [binary, {packet, 0}]),
    PushJson = make_json(Msg),
    ok = gen_tcp:send(Socket, PushJson),
    gen_tcp:close(Socket).


main() ->
    {ok, [[Host]]} = init:get_argument(h),
    {ok, [[PortStr]]} = init:get_argument(p),
    {ok, [[MsgStr]]} = init:get_argument(m),

    {Port, _} = string:to_integer(PortStr),
    %% Msg = binary:list_to_bin(MsgStr),
    Msg = unicode:characters_to_binary(MsgStr),
    io:format("~p~n", [Msg]),
    push(Host, Port, Msg).
