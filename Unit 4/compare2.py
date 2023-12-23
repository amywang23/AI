for nb in edges[city2]:
            neighbor = nb[0]
            new_distance = distances_target[city2] + nb[1]
            node1 = nodes[neighbor]
            node2 = nodes[start]
            estimate = calcd(node1, node2)
            if (new_distance < distances_target[neighbor] ):
                distances_target[neighbor] = new_distance
                newpath = list(v2[2])
                newpath.append(neighbor)
                heapq.heappush(q2, (distances_target[neighbor]+estimate, neighbor, newpath))
                visited2.add(neighbor)
                map2[neighbor] = newpath

                if neighbor in visited1:
                    list2 = map2[neighbor]
                    if len(list2) > 0:
                        list2.pop()
                        list2.reverse()
                    print("biA* meet from back distance=", distances[neighbor]+distances_target[neighbor])
                    #print("path", map1[neighbor], "-----", list2)
                    draw_final_route(map1[neighbor] + list2, r, c)
                    return
            draw_search_route(city2, neighbor, r, c)