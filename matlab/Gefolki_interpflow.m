%     « Copyright (c) 2016, Elise Koeniguer, Aurélien Plyer (Onera) » 
%     This file is part of GeFolki.
% 
%     GeFolki is free software: you can redistribute it and/or modify
%     it under the terms of the GNU General Public License as published by
%     the Free Software Foundation, either version 3 of the License, or
%     (at your option) any later version.
% 
%     GeFolki is distributed in the hope that it will be useful,
%     but WITHOUT ANY WARRANTY; without even the implied warranty of
%     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
%     GNU General Public License for more details.
% 
%     You should have received a copy of the GNU General Public License
%     along with GeFolki in the file copying.txt.  
%     If not, see <http://www.gnu.org/licenses/gpl.txt>.
%
% ------------------------------------------------------------------------
%
%     GeFolki est un logiciel libre ; vous pouvez le redistribuer ou le
%     modifier suivant les termes de la GNU General Public License telle
%     que publiée par la Free Software Foundation ; soit la version 3 de la
%     licence, soit (à votre gré) toute version ultérieure.
% 
%     GeFolki est distribué dans l'espoir qu'il sera utile, mais SANS
%     AUCUNE GARANTIE ; sans même la garantie tacite de QUALITÉ MARCHANDE
%     ou d'ADÉQUATION à UN BUT PARTICULIER. Consultez la GNU General Public
%     License pour plus de détails.
% 
%     Vous devez avoir reçu une copie de la GNU General Public License en
%     même temps que Gefolki dans le fichier copying.txt ; si ce n'est pas
%     le cas, consultez % <http://www.gnu.org/licenses/gpl.txt


function I2 = Gefolki_interpflow(Im,Is,C)

% I2 = Gefolki_interpflow(Im,Is,C)
% Input:    Im : Master Image       dimx x dimy
%           Is : Slave Image        dimx x dimy
%           C  : Flow Matrix        dimx x dimy x 3


if nargin<3
    Warning('Not enough Input in interpflow')
end

[row, col] = size(Is);
[x, y] = meshgrid(1:col, 1:row);
u = C(:,:,1);
v = C(:,:,2);
dx = x + u;
dy = y + v;

I2 = interp2(Is, dx, dy);
I2(isnan(I2)) = 0;
